import axios from "axios"
import "./App.css"
import { useState } from "react"

function App() {
  const [responseText, setResponseText] = useState("")
  function postData() {
    const indent = (document.querySelector("#indent") as HTMLInputElement).value
    const ignore = (document.querySelector("#ignore") as HTMLInputElement).value
    const files = (document.querySelector("#file") as HTMLInputElement).files
    if (files) {
      const formData = new FormData()
      formData.append("indent", indent)
      formData.append("ignore", ignore)
      formData.append("file", files[0])
      axios.post("http://127.0.0.1:8000/upload", formData).then((response) => {
        setResponseText(response.data["output"])
      })
    }
  }

  return (
    <>
      <div className="block">
        <input id="file" type="file" accept=".zip, " placeholder='Архив' />
        <input id="indent" type="number" placeholder='Отступ' />
        <input id="ignore" type="text" placeholder='Игнорируемые директории' />
        <button onClick={() => postData()}>Отправить</button>
        <div className="output" style={{ whiteSpace: "pre-line" }}>{responseText}</div>
      </div>
    </>
  )
}

export default App
