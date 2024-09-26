import GitHubButton from "react-github-btn";
import {
  Container,
  Grid,
  Header,
  Message,
  Table,
  Button,
} from "semantic-ui-react";
import ModalContentImage from "./ModalContentImage";
import { bahnhofLinks, katschhofLinks } from "./links";
import { useEffect, useState } from "react";
import {
  enable as enableDarkMode,
  disable as disableDarkMode,
} from "darkreader";

const Home = () => {
  const [darkMode, setDarkMode] = useState(true);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  useEffect(() => {
    if (darkMode) {
      enableDarkMode({});
    } else {
      disableDarkMode();
    }
  }, [darkMode]);

  return (
    <Container>
      <Grid container style={{ padding: "5em 0em" }}>
        <Grid.Row>
          <Grid.Column>
            <Header as="h1" dividing>
              Aachen Termin Bot{" "}
              <GitHubButton
                href="https://github.com/noworneverev/aachen-termin-bot"
                data-color-scheme={
                  darkMode
                    ? "no-preference: dark; light: light; dark: dark;"
                    : "no-preference: light; light: light; dark: light;"
                }
                data-icon="octicon-star"
                data-show-count="true"
                aria-label="Star noworneverev/aachen-termin-bot on GitHub"
              >
                Star
              </GitHubButton>
              <Button
                className="right floated"
                icon={darkMode ? "sun" : "moon"}
                content={
                  darkMode ? " Switch to Light Mode" : "Switch to Dark Mode"
                }
                onClick={toggleDarkMode}
              />
            </Header>
          </Grid.Column>
        </Grid.Row>

        <Grid.Row>
          <Grid.Column>
            <Message positive>
              Smooth out your appointment scheduling experience in Aachen with
              the help of notifications from respective Telegram Channels.
            </Message>
          </Grid.Column>
        </Grid.Row>

        <Grid.Row>
          <Grid.Column>
            <Header as="h1" dividing>
              SuperC Termin
            </Header>

            <Message info>
              <p>
                This channel is exclusively for students of RWTH Aachen
                University who are applying for visa extensions. Instant
                notifications will be sent to the channel once appointment slots
                become available.
              </p>
              <p>
                SuperC Termin Link (RWTH - Außenstelle Super C):{" "}
                <a
                  target="_blank"
                  rel="noreferrer"
                  href="https://termine.staedteregion-aachen.de/auslaenderamt/"
                >
                  https://termine.staedteregion-aachen.de/auslaenderamt/
                </a>
              </p>
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
                    <Table.Cell>
                      <ModalContentImage
                        imageUrl="./static/superc.jpeg"
                        description="SuperC Termin"
                      />
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
              Aachen Hbf Termin
            </Header>

            <Message info>
              <p>
                This channel is for those who need the services of the
                Ausländeramt at HBF. Instant notifications will be sent to the
                channel once appointment slots become available.
              </p>
              <p>
                Aachen Hbf Link (Aufenthalt, Team 1 to Team 3):{" "}
                <a
                  target="_blank"
                  rel="noreferrer"
                  href="https://termine.staedteregion-aachen.de/auslaenderamt/"
                >
                  https://termine.staedteregion-aachen.de/auslaenderamt/
                </a>
              </p>
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
                    <Table.Cell>Aachen Hbf Termin</Table.Cell>
                    <Table.Cell>
                      <a
                        target="_blank"
                        rel="noreferrer"
                        href="https://t.me/hbf_termin"
                      >
                        https://t.me/hbf_termin
                      </a>
                    </Table.Cell>
                    <Table.Cell>
                      <ModalContentImage
                        imageUrl="./static/hbf.png"
                        description="Aachen Hbf Termin"
                      />
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
              FH Aachen Termin
            </Header>

            <Message info>
              <p>
                This channel is exclusively for students of FH Aachen who are
                applying for visa extensions. Instant notifications will be sent
                to the channel once appointment slots become available.
              </p>
              <p>
                FH Aachen Termin Link (Fachhochschule Aachen):{" "}
                <a
                  target="_blank"
                  rel="noreferrer"
                  href="https://termine.staedteregion-aachen.de/auslaenderamt/"
                >
                  https://termine.staedteregion-aachen.de/auslaenderamt/
                </a>
              </p>
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
                    <Table.Cell>FH Aachen Termin</Table.Cell>
                    <Table.Cell>
                      <a
                        target="_blank"
                        rel="noreferrer"
                        href="https://t.me/+sCtrviN5NNw2YzBi"
                      >
                        https://t.me/+sCtrviN5NNw2YzBi
                      </a>
                    </Table.Cell>
                    <Table.Cell>
                      <ModalContentImage
                        imageUrl="./static/fh.png"
                        description="FH Aachen Termin"
                      />
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
              Abholung Aufenthaltserlaubnis Termin
            </Header>

            <Message info>
              <p>
                This channel is for Abholung Aufenthaltserlaubnis. Instant
                notifications will be sent to the channel once appointment slots
                become available.
              </p>
              <p>
                Abholung Aufenthaltserlaubnis Termin Link (Abholung):{" "}
                <a
                  target="_blank"
                  rel="noreferrer"
                  href="https://termine.staedteregion-aachen.de/auslaenderamt/"
                >
                  https://termine.staedteregion-aachen.de/auslaenderamt/
                </a>
              </p>
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
                    <Table.Cell>
                      Abholung Aufenthaltserlaubnis Termin
                    </Table.Cell>
                    <Table.Cell>
                      <a
                        target="_blank"
                        rel="noreferrer"
                        href="https://t.me/+1EGm6-NDQGM2ODAy"
                      >
                        https://t.me/+1EGm6-NDQGM2ODAy
                      </a>
                    </Table.Cell>
                    <Table.Cell>
                      <ModalContentImage
                        imageUrl="./static/abholung.png"
                        description="Abholung Aufenthaltserlaubnis Termin"
                      />
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
              Aachen Wohnsitz an-/ ab-/ ummelden Termin
            </Header>

            <Message info>
              <p>
                Every month has its own channel. Join the respective channels
                below to receive instant notifications when appointment slots
                become available at Bürgerservice Bahnhofplatz or Bürgerservice
                Katschhof.
              </p>
              <ul>
                <li>
                  <a
                    target="_blank"
                    rel="noreferrer"
                    href="https://www.qtermin.de/bahnhofplatzkatschhof?calendarid=57003,57091,57092,57093,57094,71058,71059,71060,71061,71062,77257,77289,77291,77292,133608,133610,133607,133612,133614,133615,133616"
                  >
                    Termin im Bürgerservice Bahnhofplatz vereinbaren
                  </a>
                </li>
                <li>
                  <a
                    target="_blank"
                    rel="noreferrer"
                    href="https://qtermin.de/BahnhofplatzKatschhof?calendarid=57095,57096,57097,74724,74725,133598"
                  >
                    Termin im Bürgerservice Katschhof vereinbaren
                  </a>
                </li>
              </ul>
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
                  {bahnhofLinks.map((link, index) => (
                    <Table.Row key={index}>
                      {link.month === 1 ? (
                        <Table.Cell rowSpan="12">
                          Bürgerservice Bahnhofplatz
                        </Table.Cell>
                      ) : null}

                      <Table.Cell>{link.month}</Table.Cell>
                      <Table.Cell>
                        <a
                          target="_blank"
                          rel="noreferrer"
                          href={link.inviteLink}
                        >
                          {link.inviteLink}
                        </a>
                      </Table.Cell>
                      <Table.Cell>
                        <ModalContentImage
                          imageUrl={link.qrCode}
                          description={link.description}
                        />
                      </Table.Cell>
                    </Table.Row>
                  ))}

                  {katschhofLinks.map((link, index) => (
                    <Table.Row key={index}>
                      {link.month === 1 ? (
                        <Table.Cell rowSpan="12">
                          Bürgerservice Katschhof
                        </Table.Cell>
                      ) : null}

                      <Table.Cell>{link.month}</Table.Cell>
                      <Table.Cell>
                        <a
                          target="_blank"
                          rel="noreferrer"
                          href={link.inviteLink}
                        >
                          {link.inviteLink}
                        </a>
                      </Table.Cell>
                      <Table.Cell>
                        <ModalContentImage
                          imageUrl={link.qrCode}
                          description={link.description}
                        />
                      </Table.Cell>
                    </Table.Row>
                  ))}
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
                If you find this project helpful, consider buying me a coffee
                ☕️
              </Message.Header>
              <Message.Content>
                <a
                  target="_blank"
                  rel="noreferrer"
                  href="https://www.paypal.me/liaoyanying"
                >
                  paypalme/liaoyanying
                </a>
              </Message.Content>
            </Message>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </Container>
  );
};

export default Home;
