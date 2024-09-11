export function generateVersionSchema(additionalProperties = undefined) {
    return {
        type: "object",
        properties: {
            id: {
                type: "string"
            },
            version: {
                type: "string"
            },
            ...additionalProperties
        },
        required: [
            "id",
            "version",
            ...Object.keys(additionalProperties || {})
        ]
    }
}

export const versionBaseSchema = generateVersionSchema();
