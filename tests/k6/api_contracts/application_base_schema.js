export function generateApplicationSchema(additionalProperties = undefined) {
    return {
        type: "object",
        properties: {
            id: {
                type: "string",
            },
            name: {
                type: "string",
            },
            createdAt: {
                type: "string",
            },
            modifiedAt: {
                type: "string",
            },
            ...additionalProperties
        },
        required: [
            "id",
            "name",
            "createdAt",
            "modifiedAt",
            ...Object.keys(additionalProperties || {})
        ]
    }
}

export const applicationBaseSchema = generateApplicationSchema();