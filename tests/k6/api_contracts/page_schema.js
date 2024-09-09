export const pageResponseSchema = function(item) {
    const itemSchema = item ?? { type: "object" }

    return {
    type: "object",
    properties: {
        items: {
            type: "array",
            items: itemSchema
        },
        limit: {
            type: "number"
        },
        offset: {
            type: "number"
        },
        total: {
            type: "number"
        }
    },
    required: [
        "items",
        "limit",
        "offset",
        "total",
    ]
}
}