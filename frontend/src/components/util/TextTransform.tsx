export function capitalize(str: string | undefined) {
    return str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
}

export function truncateText(text: string, maxLength: number, ending: string = '...'): string {
    return text.length > maxLength ? `${text.slice(0, maxLength)+ending}` : text;
}