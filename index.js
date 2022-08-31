
const { spawn,  execSync } = require('child_process');
const ls = spawn('./src/script/submit_job.sh');

execSync('chmod -R 777 ./src/script/submit_job.sh')

ls.stdout.on('data', (data) => {
  console.log('+++++++> data======>', `${data}`)
  console.log('parsed data', JSON.parse(`${data}`))
});

ls.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

ls.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});

