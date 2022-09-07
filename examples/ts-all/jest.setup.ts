import { toBeSameStory } from "../../src/jest_plugin";
import "../../src/jest_plugin/all";

// or just add specific matchers
expect.extend({ toBeSameStory });