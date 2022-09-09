import { toBeSameStory } from "../../src/jest_plugin";
// import "../../src/jest_plugin/all";

console.log("=========>");
// or just add specific matchers
expect.extend({ toBeSameStory });