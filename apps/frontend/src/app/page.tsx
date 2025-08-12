import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

// --- Tipagem dos Dados ---
interface CovidData {
  id: number;
  country: string;
  cases: number;
  deaths: number;
  report_date: string;
}

// --- Função de Busca de Dados ---
async function getCovidData(): Promise<CovidData[]> {
  try {
    const response = await fetch('http://localhost:5001/api/data', {
      cache: 'no-store',
    });
  
    if (!response.ok) {
      console.error("Falha ao buscar dados: ", response.statusText);
      return [];
    }
  
    return response.json();
  } catch (error) {
    console.error("Erro de conexão com a API: ", error);
    return [];
  }
}


export default async function HomePage() {
  const data = await getCovidData();

  return (
    <main className="flex min-h-screen flex-col items-center bg-gray-950 text-white p-4">
      <div className="w-full max-w-4xl">
        <h1 className="text-3xl md:text-4xl font-bold text-center mb-8">
          Painel de Dados COVID-19
        </h1>

        <div className="rounded-md border border-gray-700 overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow className="border-gray-700 hover:bg-gray-800">
                <TableHead className="font-bold text-white">País</TableHead>
                <TableHead className="font-bold text-white text-right">Casos</TableHead>
                <TableHead className="font-bold text-white text-right">Mortes</TableHead>
                <TableHead className="font-bold text-white text-right">Data do Relatório</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.length > 0 ? (
                data.map((row) => (
                  <TableRow key={row.id} className="border-gray-800 hover:bg-gray-900">
                    <TableCell>{row.country}</TableCell>
                    <TableCell className="text-right">{row.cases.toLocaleString('pt-BR')}</TableCell>
                    <TableCell className="text-right">{row.deaths.toLocaleString('pt-BR')}</TableCell>
                    <TableCell className="text-right">
                      {new Date(row.report_date).toLocaleDateString('pt-BR', { timeZone: 'UTC' })}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} className="text-center text-gray-400 py-8">
                    Nenhum dado encontrado. O backend eatá rodando?
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    </main>
  );
}
