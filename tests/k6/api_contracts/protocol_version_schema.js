import { generateVersionSchema } from "./version_base_schema.js";

export const protocolVersionSchema = generateVersionSchema({
    description: {
        type: "string",
    },
})