 function ExecPythonCommand(pythonCommand){
        var request = new XMLHttpRequest()

        request.open("POST", "/" + pythonCommand, false)
        request.send()
        fetch("http://127.0.0.1:5000/book", {
      method: "post",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },


  body: JSON.stringify({
    book: val,

  })
}).then(window.url = document.url)

    }


