import fs from 'fs';
import path from 'path';

/**
 * 获取文件的修改时间
 * @param {string} filePath - 文件路径
 * @returns {number} - 文件修改时间的时间戳
 */
export function getFileModificationTime(filePath) {
  try {
    const stats = fs.statSync(filePath);
    return stats.mtimeMs;
  } catch (error) {
    console.error(`获取文件修改时间失败: ${filePath}`, error);
    return 0;
  }
}

/**
 * 从导入路径获取实际文件路径
 * @param {string} importPath - 导入路径，如 '@content/tools/en/tool-name.md'
 * @returns {string} - 实际文件路径
 */
export function getActualFilePath(importPath) {
  // 将@content替换为实际路径
  return importPath.replace('@content', path.join(process.cwd(), 'src/content'));
}
