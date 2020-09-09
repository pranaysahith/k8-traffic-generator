import React from "react";
import Button from "react-bootstrap/Button";
import axios from "axios";
import Container from "react-bootstrap/esm/Container";

const deleteAllJobs = async () => {
  await axios.delete("/backend/jobs/processor");
};

const JobDeleter = () => {
  return (
    <Container>
      <Button variant="danger" onClick={deleteAllJobs}>
        Delete all jobs
      </Button>
    </Container>
  );
};

export default JobDeleter;
