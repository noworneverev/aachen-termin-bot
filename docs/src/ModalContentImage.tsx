import React from "react";
import { Button, Image, Modal } from "semantic-ui-react";

interface Props {
  imageUrl: string;
  description?: string;
}

function ModalContentImage({ imageUrl, description }: Props) {
  const [open, setOpen] = React.useState(false);

  return (
    <Modal
      onClose={() => setOpen(false)}
      onOpen={() => setOpen(true)}
      open={open}
      trigger={<Button>Show QR Code</Button>}
    >
      <Modal.Header>QR Code</Modal.Header>
      <Modal.Content image>
        <Image size="medium" src={imageUrl} wrapped />
        <Modal.Description>
          <p>{description}</p>
        </Modal.Description>
      </Modal.Content>
      <Modal.Actions>
        <Button size="small" onClick={() => setOpen(false)} positive>
          Ok
        </Button>
      </Modal.Actions>
    </Modal>
  );
}

export default ModalContentImage;
