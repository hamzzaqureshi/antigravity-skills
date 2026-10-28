const { spawn } = require("node:child_process");
const path = require("node:path");

const scriptsDir = path.join(__dirname, "..", "scripts");
const testFiles = ["validate-coverage-ledger.test.cjs", "validate-findings.test.cjs"];

function runTest(file) {
  return new Promise((resolve, reject) => {
    const cp = spawn(process.execPath, [path.join(scriptsDir, file)], {
      stdio: "pipe",
      cwd: scriptsDir,
    });
    let output = "";
    cp.stdout.on("data", (d) => { output += d; });
    cp.stderr.on("data", (d) => { output += d; });
    cp.on("close", (code) => {
      if (code === 0) {
        process.stdout.write(output);
        resolve();
      } else {
        process.stderr.write(output);
        reject(new Error(`Test file failed: ${file} (exit code ${code})`));
      }
    });
    cp.on("error", reject);
  });
}

Promise.all(testFiles.map(runTest))
  .then(() => {
    console.log("All validator tests passed successfully.");
  })
  .catch((err) => {
    console.error(err.message);
    process.exit(1);
  });
