import { Specification } from "./models/Specification";
import { v4 as uuidv4 } from "uuid";

const checkId: string = uuidv4();

export const mockInputData: Specification = {
  check_id: checkId,
  component: "Button",
  height: "600",
  args: [{name: "label", value: "arse"}],
  path: "Example",
  story: "Primary",
  width: "800",
  repository: "engi-network/same-story-storybook",
  url_check_frame: "",
  dataPath: "../../../same-story-api/test/data"
};


export const contactUsData: Specification = {
  check_id: checkId,
  component: "Contact Page",
  height: "600",
  path: "Pages",
  story: "Default",
  width: "800",
  repository: "engi-network/website",
  url_check_frame: "",
  dataPath: "../../../same-story-api/test/data/Contact",
  debug: true
};
