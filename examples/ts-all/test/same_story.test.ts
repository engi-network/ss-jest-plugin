import { mockInputData, contactUsData } from "../src/data";

const timeout = 60_000 * 3;

describe("Expect same story", () => {
  test("Are they the same story?", async () => {
    await expect(mockInputData).toBeSameStory();
  }, timeout);

  test("Is Contact page the same story?", async () => {
    await expect(contactUsData).toBeSameStory();
  }, timeout);

});
