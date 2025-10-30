import * as fs from 'fs';
import * as path from 'path';

function generateDay(dayNumber: number) {
  const dayString = dayNumber.toString().padStart(2, '0');
  const dayDir = path.join('src', `day_${dayString}`);
  
  // Create directory if it doesn't exist
  if (!fs.existsSync(dayDir)) {
    fs.mkdirSync(dayDir, { recursive: true });
    console.log(`Created directory: ${dayDir}`);
  } else {
    console.log(`Directory already exists: ${dayDir}`);
    return;
  }
  
  // Create index.ts with boilerplate
  const indexContent = `export const part_1 = (input: string): number => {
  // TODO: Implement part 1
  return 0;
}

export const part_2 = (input: string): number => {
  // TODO: Implement part 2
  return 0;
}
`;
  
  const indexPath = path.join(dayDir, 'index.ts');
  fs.writeFileSync(indexPath, indexContent);
  console.log(`Created: ${indexPath}`);
  
  // Create empty input.txt
  const inputPath = path.join(dayDir, 'input.txt');
  fs.writeFileSync(inputPath, '');
  console.log(`Created: ${inputPath}`);
  
  console.log(`\nDay ${dayNumber} boilerplate generated successfully!`);
}

// Get day number from command line arguments
const dayArg = process.argv[2];
if (!dayArg) {
  console.error('Please provide a day number: npm run generate <day>');
  process.exit(1);
}

const dayNumber = parseInt(dayArg, 10);
if (isNaN(dayNumber) || dayNumber < 1 || dayNumber > 25) {
  console.error('Day number must be between 1 and 25');
  process.exit(1);
}

generateDay(dayNumber);
