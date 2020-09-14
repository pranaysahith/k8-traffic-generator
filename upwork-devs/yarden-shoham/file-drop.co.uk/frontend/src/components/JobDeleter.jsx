import React from "react";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/esm/Container";

const deleteAllJobs = async () => {
  return fetch("/backend/jobs/processor", { method: "DELETE" });
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
