# Build a web application in Go (golang)

Go is getting more and more popular as the go-to language to build web applications.

This is in no small part due to its speed and application performance, as well as its portability. There are many resources on the internet to teach you how to build end to end web applications in Go, but for the most part they are either scattered in the form of isolated blog posts, or get into too much detail in the form of books.

With this tutorial, I hope to find the middle ground and provide a single resource which describes how to make a full stack web application in Go, along with sufficient test cases.

The only prerequisite for this tutorial is a beginner level understanding of the Go programming language.

## [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#full-stack-)“Full Stack” ?

We are going to build a community encyclopedia of birds. This website will :

*   Display the different entries submitted by the community, with the name and details of the bird they found.
*   Allow anyone to post a new entry about a bird that they saw.

This application will require three components :

1.  The web server
2.  The front-end (client side) app
3.  The database

[![Image showing application architecture](http://upload-images.jianshu.io/upload_images/13148580-80f4f7dfb7c173db.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)](https://www.sohamkamani.com/static/blog-golang-web-app-arch-a3973f373cbc863a85be21d1ec92a551-0877b.jpg) 

## [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#setting-up-your-environment)Setting up your environment

> This section describes how to set up your environment and project structure for the first time. If you have built another project in go, or know the standard directory structure, you can skip this section and go to the [next one](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#starting-an-http-server)

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#1-set-up-your-gopath)1\. Set up your $GOPATH

Run this command to check the current value of your `$GOPATH` environment variable :

```
echo $GOPATH
```

If you do not see a directory name, add the `GOPATH` variable to your environment (you can select any directory location you want, but it would be better if you create a new directory for this) :

```
export GOPATH="/location/of/your/gopath/directory"
```

You can paste the above line in you `.bashrc` or `.zshrc` file, in case you wish to make the variable permanent.

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#2-set-up-your-directory-structure)2\. Set up your directory structure

Hereafter, the “Go directory” will refer to the location described by your `$GOPATH` environment variable. Inside the Go directory, you will have to create 3 folders (if they are not there already) :

```
# Inside the Go directory
mkdir src
mkdir pkg
mkdir bin
```

The purpose of each directory can be seen from its name:

*   `bin` - is where all the executable binaries created by compiling your code go
*   `pkg` - Contains package objects made by libraries (which you don’t have to worry about now)
*   `src` - is where **all** your Go source code goes. Yes, all of it. Even that weird side project that you are thinking of making.

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#3-creating-your-project-directory)3\. Creating your project directory

The project folders inside the `src` directory should follow that same location structure as the place where your remote repository lies. So, for example, if I want to make a new project called “birdpedia”, and I make a repository for that under my name on github, such that the location of my project repository would be on “github.com/sohamkamani/birdpedia”, then the location of this project on my computer would be : `$GOPATH/src/github.com/sohamkamani/birdpedia`

Go ahead and make a similar directory for your project. If you haven’t made an online repo yet, just name the directories according to the location that you *plan* to put your code in.

This location on your computer will henceforth be referred to as your “project directory”

## [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#starting-an-http-server)Starting an HTTP server

Inside your project directory, create a file called `main.go` inside your project directory :

```
touch main.go
```

This file will contain the code to start your server :

```
// This is the name of our package
// Everything with this package name can see everything
// else inside the same package, regardless of the file they are in
package main

// These are the libraries we are going to use
// Both "fmt" and "net" are part of the Go standard library
import (
	// "fmt" has methods for formatted I/O operations (like printing to the console)
	"fmt"
	// The "net/http" library has methods to implement HTTP clients and servers
	"net/http"
)

func main() {
	// The "HandleFunc" method accepts a path and a function as arguments
	// (Yes, we can pass functions as arguments, and even trat them like variables in Go)
	// However, the handler function has to have the appropriate signature (as described by the "handler" function below)
	http.HandleFunc("/", handler)

	// After defining our server, we finally "listen and serve" on port 8080
	// The second argument is the handler, which we will come to later on, but for now it is left as nil,
	// and the handler defined above (in "HandleFunc") is used
	http.ListenAndServe(":8080", nil)
}

// "handler" is our handler function. It has to follow the function signature of a ResponseWriter and Request type
// as the arguments.
func handler(w http.ResponseWriter, r *http.Request) {
	// For this case, we will always pipe "Hello World" into the response writer
	fmt.Fprintf(w, "Hello World!")
}
```

> `fmt.Fprintf`, unlike the other “printf” statements you may know, takes a “writer” as its first argument. The second argument is the data that is piped into this writer. The output therefore appears according to where the writer moves it. In our case the ResponseWriter `w` writes the output as the response to the users request.

You can now run this file :

```
go run main.go
```

And navigate to [http://localhost:8080](http://localhost:8080/) in your browser, or by running the command :

```
curl localhost:8080
```

And see the output: “Hello World!”

You have now successfully started an HTTP server in Go.

## [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#making-routes)Making routes

Our server is now running, but, you might notice that we get the same “Hello World!” response *regardless of the route we hit, or the HTTP method that we use*. To see this yourself, run the following `curl` commands, and observe the response that the server gives you :

```
curl localhost:8080/some-other-route
curl -X POST localhost:8080
curl -X PUT localhost:8080/samething
```

All three commands still give you “Hello World!”

We would like to give our server a little more intelligence than this, so that we can handle a variety of paths and methods. This is where routing comes into play.

Although you can achieve this with Go’s `net/http` standard library, there are other libraries out there that provide a more idiomatic and declarative way to handle http routing.

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#installing-external-libraries)Installing external libraries

We will be installing a few external libraries through this tutorial, where the standard libraries don’t provide the features that we want.
When we install libraries, we need a way to ensure that other people who work on our code also have the same version of the library that we do.

In order to do this, we use a “package manager” tool. This tool serves a few purposes:

*   It makes sure the versions of any external libraries we install are locked down, so that breaking changes in any of the libraries do not affect our code.
*   It fetches the required external libraries and stores them locally, so that different projects can use different versions of the same library, if they need to.
*   It stores the names and versions of all our external libraries, so that others can install the same versions that we are working with on our system.

The official package manager for Go (or rather “official experiment” that is “safe for production use” as described on its homepage) is called `dep`. You can install dep by following the [setup guide](https://github.com/golang/dep#setup). You can verify its installation by running :

```
dep version
```

which should output some information on the version if successful.

To initialize package management for our project, run the command :

```
dep init
```

THis will create the `Gopkg.toml` and `Gopkg.lock` files, which are the files that are used to record and lock dependencies in our project.

Next, we install our routing library:

```
dep ensure -add github.com/gorilla/mux
```

This will add the [`gorilla/mux`](https://github.com/gorilla/mux) library to your project.

Now, we can modify our code to make use of the functionality that this library provides :

```
package main

import (
	// Import the gorilla/mux library we just installed
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	// Declare a new router
	r := mux.NewRouter()

	// This is where the router is useful, it allows us to declare methods that
	// this path will be valid for
	r.HandleFunc("/hello", handler).Methods("GET")

	// We can then pass our router (after declaring all our routes) to this method
	// (where previously, we were leaving the secodn argument as nil)
	http.ListenAndServe(":8080", r)
}

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello World!")
}
```

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#testing)Testing

Testing is an essential part of making any application “production quality”. It ensures that our application works the way that we expect it to.

Lets start by testing our handler. Create a file called `main_test.go`:

```
//main_test.go

package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHandler(t *testing.T) {
	//Here, we form a new HTTP request. This is the request that's going to be
	// passed to our handler.
	// The first argument is the method, the second argument is the route (which
	//we leave blank for now, and will get back to soon), and the third is the
	//request body, which we don't have in this case.
	req, err := http.NewRequest("GET", "", nil)

	// In case there is an error in forming the request, we fail and stop the test
	if err != nil {
		t.Fatal(err)
	}

	// We use Go's httptest library to create an http recorder. This recorder
	// will act as the target of our http request
	// (you can think of it as a mini-browser, which will accept the result of
	// the http request that we make)
	recorder := httptest.NewRecorder()

	// Create an HTTP handler from our handler function. "handler" is the handler
	// function defined in our main.go file that we want to test
	hf := http.HandlerFunc(handler)

	// Serve the HTTP request to our recorder. This is the line that actually
	// executes our the handler that we want to test
	hf.ServeHTTP(recorder, req)

	// Check the status code is what we expect.
	if status := recorder.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Check the response body is what we expect.
	expected := `Hello World!`
	actual := recorder.Body.String()
	if actual != expected {
		t.Errorf("handler returned unexpected body: got %v want %v", actual, expected)
	}
}
```

> Go uses a convention to ascertains a test file when it has the pattern `*_test.go`

To run this test, just run :

```
go test ./...
```

from your project root directory. You should see a mild message telling you that everything ran ok.

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#making-our-routing-testable)Making our routing testable

If you notice in our previous snippet, we left the “route” blank while creating our mock request using `http.newRequest`. How does this test still pass if the handler is defined only for “GET /handler” route?

Well, turns out that this test was only testing our *handler* and not the *routing to our handler*. In simpler terms, this means that the above test ensures that the request coming in will get served correctly *provided* that it’s delivered to the correct handler.

In this section, we will test this routing, so that we can be sure that each handler is mapped to the correct HTTP route.

Before we go on to test our routing, it’s necessary to make sure that our code *can* be tested for this. Modify the `main.go` file to look like this:

```
package main

import (
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
)

// The new router function creates the router and
// returns it to us. We can now use this function
// to instantiate and test the router outside of the main function
func newRouter() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/hello", handler).Methods("GET")
	return r
}

func main() {
	// The router is now formed by calling the `newRouter` constructor function
	// that we defined above. The rest of the code stays the same
	r := newRouter()
	http.ListenAndServe(":8080", r)
}

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello World!")
}
```

Once we’ve separated our route constructor function, let’s test our routing:

```
func TestRouter(t *testing.T) {
	// Instantiate the router using the constructor function that
	// we defined previously
	r := newRouter()

	// Create a new server using the "httptest" libraries `NewServer` method
	// Documentation : https://golang.org/pkg/net/http/httptest/#NewServer
	mockServer := httptest.NewServer(r)

	// The mock server we created runs a server and exposes its location in the
	// URL attribute
	// We make a GET request to the "hello" route we defined in the router
	resp, err := http.Get(mockServer.URL + "/hello")

	// Handle any unexpected error
	if err != nil {
		t.Fatal(err)
	}

	// We want our status to be 200 (ok)
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Status should be ok, got %d", resp.StatusCode)
	}

	// In the next few lines, the response body is read, and converted to a string
	defer resp.Body.Close()
	// read the body into a bunch of bytes (b)
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err)
	}
	// convert the bytes to a string
	respString := string(b)
	expected := "Hello World!"

	// We want our response to match the one defined in our handler.
	// If it does happen to be "Hello world!", then it confirms, that the
	// route is correct
	if respString != expected {
		t.Errorf("Response should be %s, got %s", expected, respString)
	}

}
```

Now we know that every time we hit the `GET /hello` route, we get a response of hello world. If we hit any other route, it should respond with a 404\. In fact, let’s write a test for precisely this requirement :

```
func TestRouterForNonExistentRoute(t *testing.T) {
	r := newRouter()
	mockServer := httptest.NewServer(r)
	// Most of the code is similar. The only difference is that now we make a
	//request to a route we know we didn't define, like the `POST /hello` route.
	resp, err := http.Post(mockServer.URL+"/hello", "", nil)

	if err != nil {
		t.Fatal(err)
	}

	// We want our status to be 405 (method not allowed)
	if resp.StatusCode != http.StatusMethodNotAllowed {
		t.Errorf("Status should be 405, got %d", resp.StatusCode)
	}

	// The code to test the body is also mostly the same, except this time, we
	// expect an empty body
	defer resp.Body.Close()
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err)
	}
	respString := string(b)
	expected := ""

	if respString != expected {
		t.Errorf("Response should be %s, got %s", expected, respString)
	}

}
```

Now that we’ve learned how to create a simple http server, we can serve static files from it for our users to interact with.

## [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#serving-static-files)Serving static files

“Static files” are the HTML, CSS, JavaScript, images, and the other static asset files that are needed to form a website.

There are 3 steps we need to take in order to make our server serve these static assets.

1.  Create static assets
2.  Modify our router to serve static assets
3.  Add tests to verify that our new server can serve static files

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#create-static-assets)Create static assets

To create static assets, create a directory in your project root directory, and name it `assets` :

```
mkdir assets
```

Next, create an HTML file inside this directory. This is the file we are going to serve, along with any other file that goes inside the `assets` directory :

```
touch assets/index.html
```

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#modify-the-router)Modify the router

Interestingly enough, the entire file server can be enabled in just adding 3 lines of code in the router. The new router constructor will look like this :

```
func newRouter() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/hello", handler).Methods("GET")

	// Declare the static file directory and point it to the
	// directory we just made
	staticFileDirectory := http.Dir("./assets/")
	// Declare the handler, that routes requests to their respective filename.
	// The fileserver is wrapped in the `stripPrefix` method, because we want to
	// remove the "/assets/" prefix when looking for files.
	// For example, if we type "/assets/index.html" in our browser, the file server
	// will look for only "index.html" inside the directory declared above.
	// If we did not strip the prefix, the file server would look for
	// "./assets/assets/index.html", and yield an error
	staticFileHandler := http.StripPrefix("/assets/", http.FileServer(staticFileDirectory))
	// The "PathPrefix" method acts as a matcher, and matches all routes starting
	// with "/assets/", instead of the absolute route itself
	r.PathPrefix("/assets/").Handler(staticFileHandler).Methods("GET")
	return r
}
```

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#testing-the-static-file-server)Testing the static file server

You cannot truly say that you have completed a feature until you have tests for it. We can test the static file server by adding another test function to `main_test.go` :

```
func TestStaticFileServer(t *testing.T) {
	r := newRouter()
	mockServer := httptest.NewServer(r)

	// We want to hit the `GET /assets/` route to get the index.html file response
	resp, err := http.Get(mockServer.URL + "/assets/")
	if err != nil {
		t.Fatal(err)
	}

	// We want our status to be 200 (ok)
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Status should be 200, got %d", resp.StatusCode)
	}

	// It isn't wise to test the entire content of the HTML file.
	// Instead, we test that the content-type header is "text/html; charset=utf-8"
	// so that we know that an html file has been served
	contentType := resp.Header.Get("Content-Type")
	expectedContentType := "text/html; charset=utf-8"

	if expectedContentType != contentType {
		t.Errorf("Wrong content type, expected %s, got %s", expectedContentType, contentType)
	}

}
```

To *actually* test your work, run the server :

```
go run main.go
```

And navigate to [http://localhost:8080/assets/](http://localhost:8080/assets/) in your browser.

### [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#making-a-simple-browser-app)Making a simple browser app

Since we need to create our bird encyclopedia, lets create a simple HTML document that displays the list of birds, and fetches the list from an API on page load, and also provides a form to update the list of birds :

```
<!DOCTYPE html>
<html lang="en">

<head>
 <title>The bird encyclopedia</title>
</head>

<body>
  <h1>The bird encyclopedia</h1>
  <!--
    This section of the document specifies the table that will
    be used to display the list of birds and their description
   -->
  <table>
    <tr>
      <th>Species</th>
      <th>Description</th>
    </tr>
    <td>Pigeon</td>
    <td>Common in cities</td>
    </tr>
  </table>
  <br/>

  <!--
    This section contains the form, that will be used to hit the
    `POST /bird` API that we will build in the next section
   -->
  <form action="/bird" method="post">
    Species:
    <input type="text" name="species">
    <br/> Description:
    <input type="text" name="description">
    <br/>
    <input type="submit" value="Submit">
  </form>

  <!--
    Finally, the last section is the script that will
    run on each page load to fetch the list of birds
    and add them to our existing table
   -->
  <script>
    birdTable = document.querySelector("table")

    /*
    Use the browsers `fetch` API to make a GET call to /bird
    We expect the response to be a JSON list of birds, of the
    form :
    [
      {"species":"...","description":"..."},
      {"species":"...","description":"..."}
    ]
    */
    fetch("/bird")
      .then(response => response.json())
      .then(birdList => {
        //Once we fetch the list, we iterate over it
        birdList.forEach(bird => {
          // Create the table row
          row = document.createElement("tr")

          // Create the table data elements for the species and
					// description columns
          species = document.createElement("td")
          species.innerHTML = bird.species
          description = document.createElement("td")
          description.innerHTML = bird.description

          // Add the data elements to the row
          row.appendChild(species)
          row.appendChild(description)
          // Finally, add the row element to the table itself
          birdTable.appendChild(row)
        })
      })
  </script>
</body>
```

## [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#adding-the-bird-rest-api-handlers)Adding the bird REST API handlers

As we can see, we will need to implement two APIs in order for this application to work:

1.  `GET /bird` - that will fetch the list of all birds currently in the system
2.  `POST /bird` - that will add an entry to our existing list of birds

For this, we will write the corresponding handlers.

Create a new file called `bird_handlers.go`, adjacent to the `main.go` file.

First, we will add the definition of the `Bird` struct and initialize a common `bird`variable:

```
type Bird struct {
	Species     string `json:"species"`
	Description string `json:"description"`
}

var birds []Bird
```

Next, define the handler to get all birds :

```
func getBirdHandler(w http.ResponseWriter, r *http.Request) {
	//Convert the "birds" variable to json
	birdListBytes, err := json.Marshal(birds)

	// If there is an error, print it to the console, and return a server
	// error response to the user
	if err != nil {
		fmt.Println(fmt.Errorf("Error: %v", err))
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	// If all goes well, write the JSON list of birds to the response
	w.Write(birdListBytes)
}
```

Next, the handler to create a new entry of birds :

```
func createBirdHandler(w http.ResponseWriter, r *http.Request) {
	// Create a new instance of Bird
	bird := Bird{}

	// We send all our data as HTML form data
	// the `ParseForm` method of the request, parses the
	// form values
	err := r.ParseForm()

	// In case of any error, we respond with an error to the user
	if err != nil {
		fmt.Println(fmt.Errorf("Error: %v", err))
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	// Get the information about the bird from the form info
	bird.Species = r.Form.Get("species")
	bird.Description = r.Form.Get("description")

	// Append our existing list of birds with a new entry
	birds = append(birds, bird)

	//Finally, we redirect the user to the original HTMl page
	// (located at `/assets/`), using the http libraries `Redirect` method
	http.Redirect(w, r, "/assets/", http.StatusFound)
}
```

The last step, is to add these handler to our router, in order to enable them to be used by our application :

```
	// These lines are added inside the newRouter() function before returning r
	r.HandleFunc("/bird", getBirdHandler).Methods("GET")
	r.HandleFunc("/bird", createBirdHandler).Methods("POST")
	return r
```

The tests for both these handlers and the routing involved are similar to the previous tests we wrote for the `GET /hello` handler and static file server, and are left as an exercise for the reader.

> If you’re lazy, you can still see the tests in the [source code](https://github.com/sohamkamani/blog_example__go_web_app/blob/master/bird_handlers_test.go)

# [](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/#adding-a-database)Adding a database

So far, we have added persistence to our application, with the information about different birds getting stored and retrieved.

However, this persistence is short lived, since it is in memory. This means that anytime you restart your application, all the data gets erased. In order to add *true* persistence, we will need to add a database to our stack.

Until now, our code was easy to reason about and test, since it was a standalone application. Adding a database will add another layer of communication.

You can read about how to integrate a postgres database into your Go application in my [next post](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/)

**You can find the source code for this post [https://github.com/sohamkamani/blog_example](https://github.com/sohamkamani/blog_example)**

## Adding a database to a Go web application

This post will go through how to add a postgres database into your Go application.

It is not enough to just add a driver and query the database in your code if you want to make your application production ready. There are a few things that you have to take care of:

1.  How would you write tests for your application?
2.  How will you ensure that everyone else who wants to run the application (including other servers and VMs) are using the same database structure as the one you developed?
3.  How do you most effectively make use of your computing resources?

First, lets start with adding the database to an existing application.

## [](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/#our-application)Our application

I have written another post on setting up a web application in Go. You can read it [here](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/), if you want to go into detail. In short, we have an encyclopedia of birds, that we have turned into a web application.

*   A user can make a `POST` call to create a new bird entry
*   Each entry consists of the *“species”* and *“description”* of the bird.
*   A user can get existing entries by fetching them through a `GET` call.

The only issue with this existing application, is that the storage is all in memory (stored in data structures within the application code itself) this means that if we restarted the application, all the data would disappear.

Additionally, since all the data is stored in memory, it’s very likely that we would run out of space quickly, since RAM is a much more limited resource as compared to disk space.

Adding a database, would help solve these issues.

## [](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/#creating-our-database-tables)Creating our database tables

First, create a database on postgres, and connect to it :

```
CREATE DATABASE bird_encyclopedia;
\c bird_encyclopedia
```

Based on our application, we can determine the column names and types for our `birds` table:

*   *“species”* which is expected to be a short string of text
*   *“description”* which is expected to be a longer string of text
*   *“id”*, which will be an autogenerated integer to keep track of our entries.

Based on this, create a new table using the postgres command line :

```
CREATE TABLE birds (
  id SERIAL PRIMARY KEY,
  bird VARCHAR(256),
  description VARCHAR(1024)
);
```

## [](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/#connecting-to-the-database-in-go)Connecting to the database in Go

We are going to structure our application in such a way, that the database will be modeled as a “store” interface within our application.

### [](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/#creating-the-store-interface-and-implementation)Creating the store interface, and implementation

Add the file `store.go` to the existing application :

```
package main

// The sql go library is needed to interact with the database
import (
	"database/sql"
)

// Our store will have two methods, to add a new bird,
// and to get all existing birds
// Each method returns an error, in case something goes wrong
type Store interface {
	CreateBird(bird *Bird) error
	GetBirds() ([]*Bird, error)
}

// The `dbStore` struct will implement the `Store` interface
// It also takes the sql DB connection object, which represents
// the database connection.
type dbStore struct {
	db *sql.DB
}

func (store *dbStore) CreateBird(bird *Bird) error {
	// 'Bird' is a simple struct which has "species" and "description" attributes
	// THe first underscore means that we don't care about what's returned from
	// this insert query. We just want to know if it was inserted correctly,
	// and the error will be populated if it wasn't
	_, err := store.db.Query("INSERT INTO birds(species, description) VALUES ($1,$2)", bird.Species, bird.Description)
	return err
}

func (store *dbStore) GetBirds() ([]*Bird, error) {
	// Query the database for all birds, and return the result to the
	// `rows` object
	rows, err := store.db.Query("SELECT species, description from birds")
	// We return incase of an error, and defer the closing of the row structure
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	// Create the data structure that is returned from the function.
	// By default, this will be an empty array of birds
	birds := []*Bird{}
	for rows.Next() {
		// For each row returned by the table, create a pointer to a bird,
		bird := &Bird{}
		// Populate the `Species` and `Description` attributes of the bird,
		// and return incase of an error
		if err := rows.Scan(&bird.Species, &bird.Description); err != nil {
			return nil, err
		}
		// Finally, append the result to the returned array, and repeat for
		// the next row
		birds = append(birds, bird)
	}
	return birds, nil
}

// The store variable is a package level variable that will be available for
// use throughout our application code
var store Store

/*
We will need to call the InitStore method to initialize the store. This will
typically be done at the beginning of our application (in this case, when the server starts up)
This can also be used to set up the store as a mock, which we will be observing
later on
*/
func InitStore(s Store) {
	store = s
}
```

There are lots of benefits to creating the store as an interface

*   We can change its implementation at any time without affecting the components that use it
*   It can be mocked in unit tests that use its implementation.

### [](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/#testing-the-store)Testing the store

Before we can use the store in our application, we will have to write tests for it. These will be more like integration tests, since they will test our interaction with the database in the process.

We will also be using a test suite, instead of the usual test functions. This is to make it easier for us to perform one-time setups before some of our tests run. This setup, as is seen in the code mainly entails making and storing the actual database connection, and cleaning up the database before the tests run.

```
package main

import (
	"database/sql"
	"testing"

	// The "testify/suite" package is used to make the test suite
	"github.com/stretchr/testify/suite"
)

type StoreSuite struct {
	suite.Suite
	/*
		The suite is defined as a struct, with the store and db as its
		attributes. Any variables that are to be shared between tests in a
		suite should be stored as attributes of the suite instance
	*/
	store *dbStore
	db    *sql.DB
}

func (s *StoreSuite) SetupSuite() {
	/*
		The database connection is opened in the setup, and
		stored as an instance variable,
		as is the higher level `store`, that wraps the `db`
	*/
	connString := "dbname=<your test db name> sslmode=disable"
	db, err := sql.Open("postgres", connString)
	if err != nil {
		s.T().Fatal(err)
	}
	s.db = db
	s.store = &dbStore{db: db}
}

func (s *StoreSuite) SetupTest() {
	/*
		We delete all entries from the table before each test runs, to ensure a
		consistent state before our tests run. In more complex applications, this
		is sometimes achieved in the form of migrations
	*/
	_, err := s.db.Query("DELETE FROM birds")
	if err != nil {
		s.T().Fatal(err)
	}
}

func (s *StoreSuite) TearDownSuite() {
	// Close the connection after all tests in the suite finish
	s.db.Close()
}

// This is the actual "test" as seen by Go, which runs the tests defined below
func TestStoreSuite(t *testing.T) {
	s := new(StoreSuite)
	suite.Run(t, s)
}

func (s *StoreSuite) TestCreateBird() {
	// Create a bird through the store `CreateBird` method
	s.store.CreateBird(&Bird{
		Description: "test description",
		Species:     "test species",
	})

	// Query the database for the entry we just created
	res, err := s.db.Query(`SELECT COUNT(*) FROM birds WHERE description='test description' AND SPECIES='test species'`)
	if err != nil {
		s.T().Fatal(err)
	}

	// Get the count result
	var count int
	for res.Next() {
		err := res.Scan(&count)
		if err != nil {
			s.T().Error(err)
		}
	}

	// Assert that there must be one entry with the properties of the bird that we just inserted (since the database was empty before this)
	if count != 1 {
		s.T().Errorf("incorrect count, wanted 1, got %d", count)
	}
}

func (s *StoreSuite) TestGetBird() {
	// Insert a sample bird into the `birds` table
	_, err := s.db.Query(`INSERT INTO birds (species, description) VALUES('bird','description')`)
	if err != nil {
		s.T().Fatal(err)
	}

	// Get the list of birds through the stores `GetBirds` method
	birds, err := s.store.GetBirds()
	if err != nil {
		s.T().Fatal(err)
	}

	// Assert that the count of birds received must be 1
	nBirds := len(birds)
	if nBirds != 1 {
		s.T().Errorf("incorrect count, wanted 1, got %d", nBirds)
	}

	// Assert that the details of the bird is the same as the one we inserted
	expectedBird := Bird{"bird", "description"}
	if *birds[0] != expectedBird {
		s.T().Errorf("incorrect details, expected %v, got %v", expectedBird, *birds[0])
	}
}
```

One point to note while writing tests that involve the use of a database (or, for that matter, any persistent store), is to always use the most direct mode of access when observing results.
In the tests above, when testing the `CreateBird` method, we queried the database directly to get the count of entires, instead of using the `GetBirds`method and seeing the length of the resulting slice of birds.
Similarly, when testing `GetBirds`, we used the `INSERT` query instead of using the `CreateBird` metgod to insert an entry into our table.

This is so that we can isolate the errors in each of our methods, and prevent false positives from occuring, should both the methods fail to run the way we expect them to.

## [](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/#adding-the-store-to-our-application)Adding the store to our application

Now that we have created and tested our database store, we can add it to our application. If you have not read the [previous post](https://www.sohamkamani.com/blog/2017/09/13/how-to-build-a-web-application-in-golang/) on creating the handlers, you can see the code [here](https://github.com/sohamkamani/blog_example__go_web_app/blob/master/bird_handlers.go) to know about the earlier implementation. There are very few changes that we actually have to make to our code to implement the store :

```
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

type Bird struct {
	Species     string `json:"species"`
	Description string `json:"description"`
}

func getBirdHandler(w http.ResponseWriter, r *http.Request) {
	/*
		The list of birds is now taken from the store instead of the package level  `birds` variable we had earlier

		The `store` variable is the package level variable that we defined in
		`store.go`, and is initialized during the initialization phase of the
		application
	*/
	birds, err := store.GetBirds()

	// Everything else is the same as before
	birdListBytes, err := json.Marshal(birds)

	if err != nil {
		fmt.Println(fmt.Errorf("Error: %v", err))
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Write(birdListBytes)
}

func createBirdHandler(w http.ResponseWriter, r *http.Request) {
	bird := Bird{}

	err := r.ParseForm()

	if err != nil {
		fmt.Println(fmt.Errorf("Error: %v", err))
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	bird.Species = r.Form.Get("species")
	bird.Description = r.Form.Get("description")

	// The only change we made here is to use the `CreateBird` method instead of
	// appending to the `bird` variable like we did earlier
	err = store.CreateBird(&bird)
	if err != nil {
		fmt.Println(err)
	}

	http.Redirect(w, r, "/assets/", http.StatusFound)
}
```

## [](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/#mocking-the-store)Mocking the store

Using the store in the request handlers was easy, as we just saw. The tricky part comes when you need to test the handlers. It would be unwise use an actual database connection for this :

*   We only want to test that the handler actually *called* the stores `GetBirds` and `CreateBird` methods with the correct arguments.
*   By using an actual database connection, our tests will not be *unit tests* since they would be implicitly testing the store as well, which would be out of its domain.

One solution to this problem is to use a mock store. The mock store will serve two purposes:

1.  It will pretend to be the actual store. By this I mean that it will accept the same arguments, and return the same type of results as the actual store implementation, without actually interacting with the database
2.  It will allow us to inspect its method calls. This is important when you want to verify that a method was called, and had the correct arguments.

The mock store is defined in a new file `store_mock.go`:

```
package main

import (
	"github.com/stretchr/testify/mock"
)

// The mock store contains additonal methods for inspection
type MockStore struct {
	mock.Mock
}

func (m *MockStore) CreateBird(bird *Bird) error {
	/*
		When this method is called, `m.Called` records the call, and also
		returns the result that we pass to it (which you will see in the
		handler tests)
	*/
	rets := m.Called(bird)
	return rets.Error(0)
}

func (m *MockStore) GetBirds() ([]*Bird, error) {
	rets := m.Called()
	/*
		Since `rets.Get()` is a generic method, that returns whatever we pass to it,
		we need to typecast it to the type we expect, which in this case is []*Bird
	*/
	return rets.Get(0).([]*Bird), rets.Error(1)
}

func InitMockStore() *MockStore {
	/*
		Like the InitStore function we defined earlier, this function
		also initializes the store variable, but this time, it assigns
		a new MockStore instance to it, instead of an actual store
	*/
	s := new(MockStore)
	store = s
	return s
}
```

Now that we have defined the mock store, we can use it in our tests:

```
package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strconv"
	"testing"
)

func TestGetBirdsHandler(t *testing.T) {
	// Initialize the mock store
	mockStore := InitMockStore()

	/* Define the data that we want to return when the mocks `GetBirds` method is
	called
	Also, we expect it to be called only once
	*/
	mockStore.On("GetBirds").Return([]*Bird{
		{"sparrow", "A small harmless bird"}
	}, nil).Once()

	req, err := http.NewRequest("GET", "", nil)

	if err != nil {
		t.Fatal(err)
	}
	recorder := httptest.NewRecorder()

	hf := http.HandlerFunc(getBirdHandler)

	// Now, when the handler is called, it should cal our mock store, instead of
	// the actual one
	hf.ServeHTTP(recorder, req)

	if status := recorder.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	expected := Bird{"sparrow", "A small harmless bird"}
	b := []Bird{}
	err = json.NewDecoder(recorder.Body).Decode(&b)

	if err != nil {
		t.Fatal(err)
	}

	actual := b[0]

	if actual != expected {
		t.Errorf("handler returned unexpected body: got %v want %v", actual, expected)
	}

	// the expectations that we defined in the `On` method are asserted here
	mockStore.AssertExpectations(t)
}

func TestCreateBirdsHandler(t *testing.T) {

	mockStore := InitMockStore()
	/*
	 Similarly, we define our expectations for th `CreateBird` method.
	 We expect the first argument to the method to be the bird struct
	 defined below, and tell the mock to return a `nil` error
	*/
	mockStore.On("CreateBird", &Bird{"eagle", "A bird of prey"}).Return(nil)

	form := newCreateBirdForm()
	req, err := http.NewRequest("POST", "", bytes.NewBufferString(form.Encode()))

	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Add("Content-Length", strconv.Itoa(len(form.Encode())))
	if err != nil {
		t.Fatal(err)
	}
	recorder := httptest.NewRecorder()

	hf := http.HandlerFunc(createBirdHandler)

	hf.ServeHTTP(recorder, req)

	if status := recorder.Code; status != http.StatusFound {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}
	mockStore.AssertExpectations(t)
}

func newCreateBirdForm() *url.Values {
	form := url.Values{}
	form.Set("species", "eagle")
	form.Set("description", "A bird of prey")
	return &form
}
```

We can visulaize the mock store, and its interaction with the rest of our code :

[图片上传失败...(image-f1331-1533133003005)]

To verify the results, run the tests with `go test`, and they should all run successfully.

## [](https://www.sohamkamani.com/blog/2017/10/18/golang-adding-database-to-web-application/#finishing-touches)Finishing touches

Now that we have tested that our store is working, *and* that our handlers are calling the store correctly, the only thing left to do is add the code for initializing the store on application start up. For this , we will edit the `main.go`file’s `main` function :

```
import (
	//...
	// The libn/pq driver is used for postgres
	_ "github.com/lib/pq"
	//...
)

func main(){
	// ...
	connString := "dbname=<your main db name> sslmode=disable"
	db, err := sql.Open("postgres", connString)

	if err != nil {
		panic(err)
	}
	err = db.Ping()

	if err != nil {
		panic(err)
	}

	InitStore(&dbStore{db: db})
	//...
}
```

The source code for this post can be found [here](https://github.com/sohamkamani/blog_example__go_web_db)
