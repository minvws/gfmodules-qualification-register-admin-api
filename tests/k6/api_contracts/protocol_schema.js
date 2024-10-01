import { protocolVersionSchema } from "./protocol_version_schema.js";

export const protocolSchema = {
    type: "object",
    properties: {
        id: {
            type: "string"
        },
        name: {
            type: "string"
        },
        description: {
            type: "string"
        },
        protocolType: {
            type: "string"
        },
        versions: {
            type: "array",
            items: protocolVersionSchema
        }
    },
    required: [
        "id",
        "name",
        "description",
        "protocolType",
        "versions"
    ]
}