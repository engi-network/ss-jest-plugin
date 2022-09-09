import { Specification } from "./models/Specification";
import { v4 as uuidv4 } from "uuid";

const checkId: string = uuidv4();

export const mockInputData: Specification = {
  check_id: checkId,
  component: "Button",
  height: "600",
  args: [{name: "label", value: "arse"}],
  path: "Example",
  story: "Primay",
  width: "800",
  repository: "engi-network/same-story-storybook",
  name: "Figma-frame-name",
  url_check_frame: ""
};
