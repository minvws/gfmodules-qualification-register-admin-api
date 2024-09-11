export const versionSchema = {
    type: "object",
    properties: {
        id: {
            type: "string"
        },
        version: {
            type: "string"
        },
    },
    required: [
        "id",
        "version",
    ]
}