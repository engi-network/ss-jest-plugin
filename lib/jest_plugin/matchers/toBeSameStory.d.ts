import { Specification } from "../../models/specification";
export declare function toBeSameStory(original: Specification): Promise<{
    pass: boolean;
    message: () => string;
}>;
