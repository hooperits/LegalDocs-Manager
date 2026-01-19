/**
 * Screenshot utility functions for documentation generation.
 *
 * Provides helpers for capturing, organizing, and validating screenshots
 * of the LegalDocs Manager application.
 */

import { Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

// Screenshot output directory (relative to repository root)
export const SCREENSHOT_BASE_DIR = path.resolve(__dirname, '../../../docs/screenshots');

// Standard viewport for all screenshots
export const VIEWPORT = { width: 1280, height: 720 };

/**
 * Options for capturing a screenshot
 */
export interface ScreenshotOptions {
  /** Screenshot filename without extension */
  name: string;
  /** Module directory name (e.g., '01-auth', '02-clients') */
  module: string;
  /** Description for README documentation */
  description: string;
  /** Capture full page instead of viewport (default: false) */
  fullPage?: boolean;
  /** CSS selector to wait for before capture */
  waitFor?: string;
  /** Additional delay in ms after page load */
  delay?: number;
}

/**
 * Information about a captured screenshot for README generation
 */
export interface ScreenshotInfo {
  filename: string;
  module: string;
  description: string;
  path: string;
  order: number;
}

// Track all captured screenshots for README generation
const capturedScreenshots: ScreenshotInfo[] = [];

/**
 * Ensure a directory exists, creating it recursively if needed
 */
export async function ensureDirectory(dirPath: string): Promise<void> {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`  Created directory: ${dirPath}`);
  }
}

/**
 * Capture a screenshot and save it to the appropriate module directory
 */
export async function captureScreenshot(
  page: Page,
  options: ScreenshotOptions
): Promise<string> {
  const { name, module, description, fullPage = false, waitFor, delay = 0 } = options;

  // Ensure module directory exists
  const moduleDir = path.join(SCREENSHOT_BASE_DIR, module);
  await ensureDirectory(moduleDir);

  // Wait for specific element if requested
  if (waitFor) {
    try {
      await page.waitForSelector(waitFor, { timeout: 10000 });
    } catch (e) {
      console.warn(`  Warning: Element ${waitFor} not found, capturing anyway`);
    }
  }

  // Additional delay if needed (for animations, etc.)
  if (delay > 0) {
    await page.waitForTimeout(delay);
  }

  // Generate filename with order prefix
  const order = capturedScreenshots.filter(s => s.module === module).length + 1;
  const filename = `${String(order).padStart(2, '0')}-${name}.png`;
  const screenshotPath = path.join(moduleDir, filename);

  // Capture screenshot
  await page.screenshot({
    path: screenshotPath,
    fullPage,
  });

  // Track for README generation
  const info: ScreenshotInfo = {
    filename,
    module,
    description,
    path: `${module}/${filename}`,
    order,
  };
  capturedScreenshots.push(info);

  console.log(`  ✓ Captured: ${info.path}`);
  return screenshotPath;
}

/**
 * Get all captured screenshots grouped by module
 */
export function getCapturedScreenshots(): Map<string, ScreenshotInfo[]> {
  const grouped = new Map<string, ScreenshotInfo[]>();

  for (const screenshot of capturedScreenshots) {
    const existing = grouped.get(screenshot.module) || [];
    existing.push(screenshot);
    grouped.set(screenshot.module, existing);
  }

  // Sort by order within each module
  for (const [module, screenshots] of grouped) {
    screenshots.sort((a, b) => a.order - b.order);
  }

  return grouped;
}

/**
 * Clear the captured screenshots list (for fresh runs)
 */
export function clearCapturedScreenshots(): void {
  capturedScreenshots.length = 0;
}

/**
 * Get total count of captured screenshots
 */
export function getScreenshotCount(): number {
  return capturedScreenshots.length;
}

/**
 * Validate that a screenshot file exists and has valid dimensions
 */
export async function validateScreenshot(screenshotPath: string): Promise<boolean> {
  if (!fs.existsSync(screenshotPath)) {
    console.error(`  ✗ Missing: ${screenshotPath}`);
    return false;
  }

  const stats = fs.statSync(screenshotPath);
  if (stats.size < 1000) {
    console.error(`  ✗ Too small: ${screenshotPath} (${stats.size} bytes)`);
    return false;
  }

  return true;
}

/**
 * Log progress message with consistent formatting
 */
export function logProgress(message: string): void {
  console.log(`\n📸 ${message}`);
}

/**
 * Log module start
 */
export function logModuleStart(moduleName: string): void {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`📁 Module: ${moduleName}`);
  console.log(`${'='.repeat(60)}`);
}

/**
 * Log completion summary
 */
export function logSummary(): void {
  const grouped = getCapturedScreenshots();
  console.log(`\n${'='.repeat(60)}`);
  console.log(`📊 Screenshot Generation Summary`);
  console.log(`${'='.repeat(60)}`);

  for (const [module, screenshots] of grouped) {
    console.log(`  ${module}: ${screenshots.length} screenshots`);
  }

  console.log(`${'─'.repeat(60)}`);
  console.log(`  Total: ${getScreenshotCount()} screenshots`);
  console.log(`${'='.repeat(60)}\n`);
}
