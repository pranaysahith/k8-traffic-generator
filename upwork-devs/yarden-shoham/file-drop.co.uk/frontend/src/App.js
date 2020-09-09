import React from "react";
import Container from "react-bootstrap/Container";
import Jumbotron from "react-bootstrap/Jumbotron";
import FileUploader from "./components/FileUploader";
import PodViewer from "./components/PodViewer";
import "./App.css";
import JobDeleter from "./components/JobDeleter";

function App() {
  return (
    <Container>
      <Jumbotron>
        <h1>Traffic Generator</h1>
        <FileUploader />
      </Jumbotron>
      <JobDeleter />
      <PodViewer />
    </Container>
  );
}

export default App;
