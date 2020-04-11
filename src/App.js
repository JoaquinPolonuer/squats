import React, { Component } from "react";
import logo from "./logo.svg";
import "./App.css";
import {
  Container,
  Navbar,
  NavbarBrand,
  Row,
  Col,
  Jumbotron,
  InputGroup,
  Input,
  Button,
  InputGroupAddon,
  FormGroup,
} from "reactstrap";
let { PythonShell } = require("python-shell");

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      Position: "Up",
      set: 0,
      Count: 0,
    };
  }
  componentDidMount() {
    this.timer = setInterval(() => this.fecthInfo(), 100);
  }
  async fecthInfo() {
    fetch("http://127.0.0.1:5000/info", { method: "GET" })
      .then((response) => response.json())
      .then((responseData) => {
        //set your data here
        this.setState({
          Count: responseData.counter,
          Position: responseData.status,
        });
        console.log(responseData);
      })
      .catch((error) => {
        console.error(error);
      });
  }
  render(props) {
    return (
      <div>
        <Navbar dark color="dark">
          <NavbarBrand href="/"> Squat</NavbarBrand>
        </Navbar>
        <Row>
          <Col xs={9} className="main"></Col>
          <Col className="sideBar">
            <Col>
              <h3 className="centered" id="tit">
                Position
              </h3>
              <h1 className="centered" id="bod">
                {this.state.Position}
              </h1>
            </Col>
            <Col>
              <h3 className="centered" id="tit">
                Current set
              </h3>
              <h1 className="centered" id="bod">
                {this.state.set}
              </h1>
            </Col>
            <Col>
              <h3 className="centered" id="tit">
                Count
              </h3>
              <h1 className="centered" id="bod">
                {this.state.Count}
              </h1>
            </Col>
            <Col className="centered">
              <Button className="but" color="primary" onClick={this.submit}>
                Start!
              </Button>
            </Col>
          </Col>
        </Row>
      </div>
    );
  }
}

export default App;
