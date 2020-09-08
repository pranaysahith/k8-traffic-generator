import React, { Component } from "react";
import Table from "react-bootstrap/Table";
import axios from "axios";

class PodViewer extends Component {
  state = { pods: [] };

  constructor() {
    super();
    setInterval(this.getPods, 1000);
  }

  renderPod = (pod) => {
    let brand;
    switch (pod.phase) {
      case "Pending":
        brand = "warning";
        break;
      case "Running":
        brand = "primary";
        break;
      case "Succeeded":
        brand = "success";
        break;
      case "Failed":
        brand = "danger";
        break;
      default:
        brand = "secondary";
        break;
    }
    const phaseClass = `text-${brand}`;
    return (
      <tr key={pod.filename}>
        <td>{pod.filename}</td>
        <td className={phaseClass}>{pod.phase}</td>
      </tr>
    );
  };

  getPods = async () => {
    try {
      const { data } = await axios.get("/backend/pods/processor");
      this.setState({ pods: data });
    } catch (error) {
      console.error(error);
    }
  };

  render() {
    return (
      <Table>
        <thead>
          <th>File Name</th>
          <th>Phase</th>
        </thead>
        <tbody>{this.state.pods.map(this.renderPod)}</tbody>
      </Table>
    );
  }
}

export default PodViewer;
