function onScanSuccess(decodedText, decodedResult) {
    console.log(`code Matched = ${decodedText}`, decodedResult);
}

function onScanFailure(error) {
    console.warn(`Code scan error = ${error}`);
}