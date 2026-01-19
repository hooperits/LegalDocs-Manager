/**
 * Test data generator for screenshot documentation.
 *
 * Creates realistic sample data (clients, cases, documents) to populate
 * the application before capturing screenshots.
 */

import { APIRequestContext } from '@playwright/test';
import {
  AuthHelper,
  API_BASE,
  generateTestClient,
  generateTestCase,
  createTestPDF,
  Client,
  Case,
  Document,
} from '../fixtures/auth';

/**
 * Complete test data set for documentation screenshots
 */
export interface TestDataSet {
  user: {
    username: string;
    email: string;
    token: string;
    userId: number;
  };
  clients: Client[];
  cases: Case[];
  documents: Document[];
}

/**
 * Sample data with realistic Spanish names for legal context
 */
const SAMPLE_CLIENTS = [
  {
    full_name: 'María García López',
    identification_number: 'DNI-12345678A',
    email: 'maria.garcia@ejemplo.com',
    phone: '+34 612 345 678',
    address: 'Calle Mayor 123, 28001 Madrid',
    is_active: true,
    notes: 'Cliente desde 2023. Casos de derecho civil.',
  },
  {
    full_name: 'Carlos Rodríguez Martínez',
    identification_number: 'DNI-87654321B',
    email: 'carlos.rodriguez@ejemplo.com',
    phone: '+34 698 765 432',
    address: 'Avenida de la Constitución 45, 41001 Sevilla',
    is_active: true,
    notes: 'Empresa PYME. Asesoría mercantil.',
  },
  {
    full_name: 'Ana Fernández Ruiz',
    identification_number: 'DNI-11223344C',
    email: 'ana.fernandez@ejemplo.com',
    phone: '+34 655 123 456',
    address: 'Plaza del Sol 7, 08001 Barcelona',
    is_active: true,
    notes: 'Derecho laboral y contratos.',
  },
];

const SAMPLE_CASES = [
  {
    title: 'Reclamación por despido improcedente',
    description: 'Cliente despedido sin causa justificada. Reclamación de indemnización y salarios de tramitación.',
    case_type: 'laboral',
    status: 'en_proceso',
    priority: 'alta',
  },
  {
    title: 'Constitución de Sociedad Limitada',
    description: 'Asesoramiento y tramitación para la constitución de una nueva SL dedicada a servicios tecnológicos.',
    case_type: 'mercantil',
    status: 'en_proceso',
    priority: 'media',
  },
  {
    title: 'Revisión de contrato de arrendamiento',
    description: 'Análisis y modificación de cláusulas en contrato de alquiler de local comercial.',
    case_type: 'civil',
    status: 'pendiente',
    priority: 'baja',
  },
  {
    title: 'Herencia y testamento',
    description: 'Gestión de herencia tras fallecimiento. Reparto de bienes según testamento.',
    case_type: 'civil',
    status: 'cerrado',
    priority: 'media',
  },
];

/**
 * Create all test data needed for documentation screenshots
 */
export async function createTestData(request: APIRequestContext): Promise<TestDataSet> {
  console.log('\n📦 Creating test data for screenshots...');

  const auth = new AuthHelper(request);

  // Register a new user for this session
  console.log('  Creating test user...');
  const registerResponse = await auth.register({
    username: `doc_user_${Date.now()}`,
    email: `doc_user_${Date.now()}@test.com`,
    password: 'DocPassword123!',
  });

  const testData: TestDataSet = {
    user: {
      username: registerResponse.user.username,
      email: registerResponse.user.email,
      token: registerResponse.token,
      userId: registerResponse.user.id,
    },
    clients: [],
    cases: [],
    documents: [],
  };

  // Create sample clients
  console.log('  Creating sample clients...');
  for (const clientData of SAMPLE_CLIENTS) {
    const response = await auth.post(`${API_BASE}/clients/`, {
      ...clientData,
      identification_number: `${clientData.identification_number}-${Date.now()}`,
    });

    if (response.status() === 201) {
      const client = await response.json() as Client;
      testData.clients.push(client);
      console.log(`    ✓ Client: ${client.full_name}`);
    }
  }

  // Create sample cases (associated with clients)
  console.log('  Creating sample cases...');
  for (let i = 0; i < SAMPLE_CASES.length && i < testData.clients.length; i++) {
    const caseData = SAMPLE_CASES[i];
    const client = testData.clients[i % testData.clients.length];

    const today = new Date().toISOString().split('T')[0];
    const deadline = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

    const response = await auth.post(`${API_BASE}/cases/`, {
      ...caseData,
      client: client.id,
      start_date: today,
      deadline: deadline,
    });

    if (response.status() === 201) {
      const caseObj = await response.json() as Case;
      testData.cases.push(caseObj);
      console.log(`    ✓ Case: ${caseObj.case_number} - ${caseObj.title}`);
    }
  }

  // Create sample documents (associated with cases)
  console.log('  Creating sample documents...');
  if (testData.cases.length > 0) {
    const documentTitles = [
      'Contrato de trabajo original',
      'Carta de despido',
      'Estatutos sociales',
    ];

    for (let i = 0; i < documentTitles.length && i < testData.cases.length; i++) {
      const caseObj = testData.cases[i];
      const pdfBuffer = createTestPDF();

      const response = await auth.uploadFile(
        `${API_BASE}/documents/`,
        pdfBuffer,
        `documento_${i + 1}.pdf`,
        {
          case: caseObj.id.toString(),
          title: documentTitles[i],
          document_type: 'contrato',
          description: `Documento de prueba para ${caseObj.title}`,
          is_confidential: 'false',
        }
      );

      if (response.status() === 201) {
        const doc = await response.json() as Document;
        testData.documents.push(doc);
        console.log(`    ✓ Document: ${doc.title}`);
      }
    }
  }

  console.log(`\n✅ Test data created:`);
  console.log(`   - 1 user: ${testData.user.username}`);
  console.log(`   - ${testData.clients.length} clients`);
  console.log(`   - ${testData.cases.length} cases`);
  console.log(`   - ${testData.documents.length} documents`);

  return testData;
}

/**
 * Clean up test data after screenshot generation (optional)
 */
export async function cleanupTestData(
  request: APIRequestContext,
  testData: TestDataSet
): Promise<void> {
  console.log('\n🧹 Cleaning up test data...');

  const auth = new AuthHelper(request);
  auth.setToken(testData.user.token);

  // Delete documents first (due to foreign key constraints)
  for (const doc of testData.documents) {
    try {
      await auth.delete(`${API_BASE}/documents/${doc.id}/`);
      console.log(`  ✓ Deleted document: ${doc.title}`);
    } catch (e) {
      console.log(`  ⚠ Could not delete document: ${doc.title}`);
    }
  }

  // Delete cases
  for (const caseObj of testData.cases) {
    try {
      await auth.delete(`${API_BASE}/cases/${caseObj.id}/`);
      console.log(`  ✓ Deleted case: ${caseObj.case_number}`);
    } catch (e) {
      console.log(`  ⚠ Could not delete case: ${caseObj.case_number}`);
    }
  }

  // Delete clients
  for (const client of testData.clients) {
    try {
      await auth.delete(`${API_BASE}/clients/${client.id}/`);
      console.log(`  ✓ Deleted client: ${client.full_name}`);
    } catch (e) {
      console.log(`  ⚠ Could not delete client: ${client.full_name}`);
    }
  }

  console.log('✅ Cleanup complete');
}

/**
 * Get auth helper with existing token
 */
export function getAuthHelper(request: APIRequestContext, token: string): AuthHelper {
  const auth = new AuthHelper(request);
  auth.setToken(token);
  return auth;
}
