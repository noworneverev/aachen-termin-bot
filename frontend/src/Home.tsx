import GitHubButton from "react-github-btn";
import {
  Container,
  Divider,
  Grid,
  Header,
  Image,
  Message,
  Segment,
  Table,
} from "semantic-ui-react";

const Home = () => (
  <>
    <Grid container style={{ padding: "5em 0em" }}>
      <Grid.Row>
        <Grid.Column>
          <Header as="h1" dividing>
            Aachen Termin Bot{" "}
            <GitHubButton
              href="https://github.com/noworneverev/aachen-termin-bot"
              data-icon="octicon-star"
              data-show-count="true"
              aria-label="Star noworneverev/aachen-termin-bot on GitHub"
            >
              Star
            </GitHubButton>
          </Header>
        </Grid.Column>
      </Grid.Row>

      <Grid.Row>
        <Grid.Column>
          <Message positive>
            Smooth out your appointment scheduling experience in Aachen with the
            help of my Telegram Channels.
          </Message>
        </Grid.Column>
      </Grid.Row>

      <Grid.Row>
        <Grid.Column>
          <Header as="h1">SuperC Termin</Header>
          <Divider />

          <Message info>
            This channel is exclusively for students of RWTH Aachen University
            who are applying for visa extensions. Instant notifications will be
            sent to the channel once appointment slots become available.
          </Message>
          <Grid.Column width={16}>
            <Table celled structured>
              <Table.Header>
                <Table.Row>
                  <Table.HeaderCell rowSpan="2">
                    Telegram Channel Name
                  </Table.HeaderCell>
                  <Table.HeaderCell rowSpan="2">Invite Link</Table.HeaderCell>
                  <Table.HeaderCell rowSpan="2">QR Code</Table.HeaderCell>
                </Table.Row>
              </Table.Header>

              <Table.Body>
                <Table.Row>
                  <Table.Cell>SuperC Termin</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/aachen_termin"
                    >
                      https://t.me/aachen_termin
                    </a>
                  </Table.Cell>
                  <Table.Cell textAlign="right">
                    <Image src="/static/superc.jpeg" size="small" />
                  </Table.Cell>
                </Table.Row>
              </Table.Body>
            </Table>
          </Grid.Column>
        </Grid.Column>
      </Grid.Row>

      <Grid.Row>
        <Grid.Column>
          <Header as="h1">Aachen Wohnsitz an-/ ab-/ ummelden Termin</Header>
          <Divider />

          <Message info>
            Every month has its own channel. Join the respective channels below
            to receive instant notifications when appointment slots become
            available at Bürgerservice Bahnhofplatz or Bürgerservice Katschhof.
          </Message>
          <Grid.Column width={16}>
            <Table celled structured>
              <Table.Header>
                <Table.Row>
                  <Table.HeaderCell rowSpan="2">Location</Table.HeaderCell>
                  <Table.HeaderCell rowSpan="2">Month</Table.HeaderCell>
                  <Table.HeaderCell rowSpan="2">Invite Link</Table.HeaderCell>
                  <Table.HeaderCell rowSpan="2">QR Code</Table.HeaderCell>
                </Table.Row>
              </Table.Header>

              <Table.Body>
                <Table.Row>
                  <Table.Cell rowSpan="12">
                    Bürgerservice Bahnhofplatz
                  </Table.Cell>
                  <Table.Cell>1</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>2</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>3</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>4</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>5</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>6</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>7</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>8</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>9</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/+4a4fC9-Kojs2OGUy"
                    >
                      https://t.me/+4a4fC9-Kojs2OGUy
                    </a>
                  </Table.Cell>
                  <Table.Cell>
                    <Image src="/static/bah9.png" size="small" />
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>10</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/+kiMHqloCLek3OWYy"
                    >
                      https://t.me/+kiMHqloCLek3OWYy
                    </a>
                  </Table.Cell>
                  <Table.Cell>
                    <Image src="/static/bah10.png" size="small" />
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>11</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/+Svisobbp7Ro5MDYy"
                    >
                      https://t.me/+Svisobbp7Ro5MDYy
                    </a>
                  </Table.Cell>
                  <Table.Cell>
                    <Image src="/static/bah11.png" size="small" />
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>12</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/+yOoYSrPiCeE0ODdi"
                    >
                      https://t.me/+yOoYSrPiCeE0ODdi
                    </a>
                  </Table.Cell>
                  <Table.Cell>
                    <Image src="/static/bah12.png" size="small" />
                  </Table.Cell>
                </Table.Row>

                <Table.Row>
                  <Table.Cell rowSpan="12">Bürgerservice Katschhof</Table.Cell>
                  <Table.Cell>1</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>2</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>3</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>4</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>5</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>6</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>7</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>8</Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                  <Table.Cell>
                    <i>upcoming...</i>
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>9</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/+W9hjKx_btwJkNzky"
                    >
                      https://t.me/+W9hjKx_btwJkNzky
                    </a>
                  </Table.Cell>
                  <Table.Cell>
                    <Image src="/static/kat9.png" size="small" />
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>10</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/+Pxy0moX0wx1iYWVi"
                    >
                      https://t.me/+Pxy0moX0wx1iYWVi
                    </a>
                  </Table.Cell>
                  <Table.Cell>
                    <Image src="/static/kat10.png" size="small" />
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>11</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/+N8d35jHjkqdiMWFi"
                    >
                      https://t.me/+N8d35jHjkqdiMWFi
                    </a>
                  </Table.Cell>
                  <Table.Cell>
                    <Image src="/static/kat11.png" size="small" />
                  </Table.Cell>
                </Table.Row>
                <Table.Row>
                  <Table.Cell>12</Table.Cell>
                  <Table.Cell>
                    <a
                      target="_blank"
                      rel="noreferrer"
                      href="https://t.me/+L6l4eytXD9cyZGNi"
                    >
                      https://t.me/+L6l4eytXD9cyZGNi
                    </a>
                  </Table.Cell>
                  <Table.Cell>
                    <Image src="/static/kat12.png" size="small" />
                  </Table.Cell>
                </Table.Row>
              </Table.Body>
            </Table>
          </Grid.Column>
        </Grid.Column>
      </Grid.Row>

      <Grid.Row>
        <Grid.Column>
          <Header as="h1" dividing>
            Github Repository
          </Header>
          <a
            href="https://github.com/noworneverev/aachen-termin-bot"
            target="_blank"
            rel="noreferrer"
          >
            https://github.com/noworneverev/aachen-termin-bot
          </a>
        </Grid.Column>
      </Grid.Row>

      <Grid.Row>
        <Grid.Column>
          <Header as="h1" dividing>
            Donate
          </Header>
          <Message info>
            <Message.Header>
              If you find this project helpful, consider buying me a coffee ☕️
            </Message.Header>
            <Message.Content>
              <a href="https://www.paypal.com/paypalme/yanyingliao">
                paypalme/yanyingliao
              </a>
            </Message.Content>
          </Message>
        </Grid.Column>
      </Grid.Row>
    </Grid>
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
  </>
);

export default Home;
