export function generateVendorSchema(additionalProperties = undefined) {
    return {
        type: "object",
        properties: {
            id: {
                type: "string",
            },
            tradeName: {
                type: "string",
            },
            statutoryName: {
                type: "string",
            },
            kvkNumber: {
                type: "string",
            },
            ...additionalProperties
        },
        required: [
            "id",
            "tradeName",
            "statutoryName",
            "kvkNumber",
            ...Object.keys(additionalProperties || {})
        ]
    }
}

export const vendorBaseSchema = generateVendorSchema();