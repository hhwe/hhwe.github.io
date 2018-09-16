## 问题

为了扩展到大型代码库，Go程序必须是轻量级的，[不会过度重复](https://www.youtube.com/watch?v=5kj5ApnhPAE)，并且还要健壮，在出现[错误](https://www.youtube.com/watch?v=lsBF58Q-DnY)时[优雅地处理错误](https://www.youtube.com/watch?v=lsBF58Q-DnY)。

在Go的设计中，我们有意识地选择使用显式错误结果和显式错误检查。相比之下，C通常使用显式检查隐式错误结果[errno](http://man7.org/linux/man-pages/man3/errno.3.html)，而在许多语言中发现的异常处理（包括C ++，C＃，Java和Python）表示隐式检查隐式结果。

例如，考虑一下这个代码，用一个假设的Go方言编写，但有例外：
```go
func CopyFile(src, dst string) throws error {
	r := os.Open(src)
	defer r.Close()

	w := os.Create(dst)
	io.Copy(w, r)
	w.Close()
}
```

这是一个很好，干净，优雅的代码。它也有无形的错误：如果`io.Copy`或`w.Close`失败，代码不会删除部分写入的`dst`文件。

另一方面，在Golang1中实际Go代码将是：
```go
func CopyFile(src, dst string) error {
	r, err := os.Open(src)
	if err != nil {
		return err
	}
	defer r.Close()

	w, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer w.Close()

	if _, err := io.Copy(w, r); err != nil {
		return err
	}
	if err := w.Close(); err != nil {
		return err
	}
}
```
这段代码不好，不干净，不优雅，而且仍然是错误的：像以前的版本一样，当`io.Copy`或`w.Close`失败它不会删除`dst`。有一种看似合理的观点认为，至少可见的检查可以促使细心的读者在代码中对适当的错误处理响应进行思考。然而，在实践中，错误检查占用了太多的空间，以至于读者很快就学会跳过它们来查看代码的结构。

此代码在其错误处理方面也有第二个遗漏。函数通常应该在错误中[包含有关](https://golang.org/doc/effective_go.html#errors)其参数的[相关信息](https://golang.org/doc/effective_go.html#errors)，例如`os.Open`返回正在打开的文件的名称。返回未修改的错误会导致失败，而不会导致导致错误的操作序列的任何信息。

简而言之，这个Go代码有太多的错误检查和错误处理。更强大的版本和更有用的错误将是：

```go
func CopyFile(src, dst string) error {
	r, err := os.Open(src)
	if err != nil {
		return fmt.Errorf("copy %s %s: %v", src, dst, err)
	}
	defer r.Close()

	w, err := os.Create(dst)
	if err != nil {
		return fmt.Errorf("copy %s %s: %v", src, dst, err)
	}

	if _, err := io.Copy(w, r); err != nil {
		w.Close()
		os.Remove(dst)
		return fmt.Errorf("copy %s %s: %v", src, dst, err)
	}

	if err := w.Close(); err != nil {
		os.Remove(dst)
		return fmt.Errorf("copy %s %s: %v", src, dst, err)
	}
}
```

纠正这些错误只会使代码更正确，更清晰或更优雅。

## 目标

对于Go 2，我们希望使错误检查更轻量级，减少专用于错误检查的Go程序文本的数量。我们还希望能够更方便地编写错误处理，从而提高程序员花时间做这件事的可能性。

错误检查和错误处理都必须保持显式，这在程序文本中是可见的。我们不想重复异常处理的陷阱。现有代码必须继续工作并保持与现在一样有效。任何更改都必须与现有代码互操作。


如上所述，该草案设计的目标不是改变或增加错误的语义。有关该讨论，请参阅[错误值问题概述](https://go.googlesource.com/proposal/+/master/design/go2draft-error-values-overview.md)。

## 设计草案

本节快速总结了设计草案，作为高级别讨论和与其他方法比较的基础。

草案设计引入了两种新的句法形式。首先，它引入了一个检查表达式，`check f(x, y, z)`或`check err`标记一个显式错误检查。其次，它引入了一个`handle`定义错误处理程序的语句。当错误检查失败时，它将控制转移到最内层处理程序，该处理程序将控制转移到它上面的下一个处理程序，依此类推，直到处理程序执行`return`语句。

例如，上面更正的代码缩短为：

```go
func CopyFile(src, dst string) error {
	handle err {
		return fmt.Errorf("copy %s %s: %v", src, dst, err)
	}

	r := check os.Open(src)
	defer r.Close()

	w := check os.Create(dst)
	handle err {
		w.Close()
		os.Remove(dst) // (only if a check fails)
	}

	check io.Copy(w, r)
	check w.Close()
	return nil
}
```

该`check`/ `handle`组合被允许在本身不返回错误的功能。例如，这是一个[有用但很简单的程序](https://github.com/rsc/tmp/blob/master/unhex/main.go)的主要功能：

```go
func main() {
	hex, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		log.Fatal(err)
	}

	data, err := parseHexdump(string(hex))
	if err != nil {
		log.Fatal(err)
	}

	os.Stdout.Write(data)
}
```

改为更短更清晰：

```go
func main() {
	handle err {
		log.Fatal(err)
	}

	hex := check ioutil.ReadAll(os.Stdin)
	data := check parseHexdump(string(hex))
	os.Stdout.Write(data)
}
```

有关详细信息，请参阅[草图设计](https://go.googlesource.com/proposal/+/master/design/go2draft-error-handling.md)。

## [](https://go.googlesource.com/proposal/+/master/design/go2draft-error-handling-overview.md#Discussion-and-Open-Questions)[](https://go.googlesource.com/proposal/+/master/design/go2draft-error-handling-overview.md#discussion-and-open-questions)讨论和开放式问题

这些草案设计仅作为社区讨论的起点。我们完全希望根据反馈，特别是经验报告修改细节。本节概述了一些有待回答的问题。

**check verus try**。关键字`check`清楚地表明了正在做什么。最初我们使用了众所周知的异常关键字`try`。这对于函数调用来说读得很好：

```go
data := try parseHexdump(string(hex))
```

但是对于应用于错误值的检查，它读得不好：

```go
data, err := parseHexdump(string(hex))
if err == ErrBadHex {
	... special handling ...
}
try err
```

在这种情况下，`check err`是一个更清晰的描述`try err`。Rust最初用于`try!`标记显式错误检查，但转移到特殊`?`运算符。斯威夫特还使用`try`标注明确的错误检查，而且还`try!`和`try?`，并为更广泛的比喻异常处理，其中还包括部分`throw`和`catch`。

总体看来，设计项目的`check`/ `handle`是从异常处理和生锈及斯威夫特十分不同的理由更清晰的关键字`check`，在比较熟悉的一个，`try`。

**defer**: 错误处理在某些方面类似于[`defer`](https://golang.org/ref/spec#Defer_statements)和[`recover`](https://golang.org/ref/spec#Handling_panics)，但是对于错误而不是恐慌。当前的草图设计使错误处理程序在词汇上链接，同时`defer`在运行时根据执行的代码构建链。这种差异对于在条件体和循环中声明的处理程序（或延迟函数）很重要。虽然错误处理程序的词汇堆叠似乎是一个稍微好一点的设计，但`defer`完全匹配可能不那么令人惊讶。作为一个例子，`defer`类似处理将更方便，如果`CopyFile`将其目的地建立`w`为其中一个`os.Stdout`或其结果`os.Create`，那么能够`os.Remove(dst)`有条件地引入处理程序将是有帮助的。

**panic**: 我们花了一些时间来尝试协调错误处理和恐慌，因此由于恐慌而不需要重复由于错误处理而进行的清理以进行清理。我们统一两者的所有尝试只会导致更多的复杂性。

**feedback**: 最有用的一般反馈将是草图设计启用或禁止的有趣用途的示例。我们也欢迎有关上述要点的反馈，特别是基于真实程序中复杂或错误错误处理的经验。

我们正在[golang.org/wiki/Go2ErrorHandlingFeedback](https://golang.org/wiki/Go2ErrorHandlingFeedback)收集反馈链接。
