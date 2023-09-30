import React from "react";
import { Segment, Container } from "semantic-ui-react";

function Footer() {
  return (
    <Segment
      inverted
      style={{ margin: "5em 0em 0em", padding: "5em 0em" }}
      vertical
    >
      <Container textAlign="center">
        {"Made with ❤️ by "}
        <a
          target="_blank"
          href={"https://noworneverev.github.io"}
          rel="noreferrer"
        >
          Yan-Ying Liao
        </a>
      </Container>
    </Segment>
  );
}

export default Footer;
