import React from "react";
import Container from "react-bootstrap/Container";
import Jumbotron from "react-bootstrap/Jumbotron";
import FileUploader from "./FileUploader";
import PodViewer from "./PodViewer";
import "./App.css";

function App() {
  return (
    <Container>
      <Jumbotron>
        <h1>Traffic Generator</h1>
        <FileUploader />
      </Jumbotron>
      <PodViewer />
    </Container>
  );
}

export default App;
