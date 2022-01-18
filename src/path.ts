
function getDataDir(): string | undefined {
    const splitPath = window.location.pathname.split("/").filter(p => p.length > 0)
    if(splitPath.length >= 1) {
        return splitPath[0]
    } else {
        return undefined
    }
}

export {getDataDir}