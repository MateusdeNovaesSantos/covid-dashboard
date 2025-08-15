"use client";

import { useState, useEffect } from "react";

// --- shadcn ---
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button";
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

// --- api ---
import { getCountries, getPaginatedData, CovidData, PaginationInfo } from "@/lib/api"

export default function HomePage() {
  // --- ESTADOS ---
  const [data, setData] = useState<CovidData[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [countries, setCountries] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [selectedCountry, setSelectedCountry] = useState("all");

  // --- FETCH DATA ---
  useEffect(() => {
    const fetchData = async() => {
      setIsLoading(true);
      const result = await getPaginatedData(currentPage, selectedCountry);
      setData(result.data);
      setPagination(result.pagination);
      setIsLoading(false);
    };

    fetchData();
  }, [currentPage, selectedCountry]);

  useEffect(() => {
    const fetchCountries = async () => {
      const countryList = await getCountries();
      setCountries(countryList);
    }

    fetchCountries();
  }, [])

  // --- FUNÇÕES DE MANIPULAÇÃO DE EVENTOS ---
  const handleNextPage = () => {
    if (pagination && pagination.has_next) {
      setCurrentPage(currentPage + 1);
    }
  }

  const handlePrevPage = () => {
    if (pagination && pagination.has_prev) {
      setCurrentPage(currentPage - 1);
    }
  }

  const handleCountryChange = (country: string) => {
    setSelectedCountry(country);
    setCurrentPage(1);
  }

  // --- JSX ---
  return (
    <main className="flex min-h-screen flex-col items-center bg-gray-950 text-white p-4">
      <div className="w-full max-w-4xl">
        <h1 className="text-3xl md:text-4xl font-bold text-center mb-8">
          Painel de Dados COVID-19
        </h1>

        {/* BARRA DE FILTROS */}
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <Select value={selectedCountry} onValueChange={handleCountryChange}>
            <SelectTrigger className="w-full md:w-[280px] bg-gray-800 border-gray-700">
              <SelectValue placeholder="Filtrar por país..." />
            </SelectTrigger>
            <SelectContent className="bg-gray-800 text-white border-gray-700">
              <SelectItem value="all">Todos os Países</SelectItem>
              {countries.map((country) => (
                <SelectItem key={country} value={country}>
                  {country}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>


        {/* TABELA DE DADOS */}
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

        {/* CONTROLES DE PAGINAÇÃO */}
        <div className="flex items-center justify-between mt-6">
          <Button
            onClick={handlePrevPage}
            disabled={!pagination?.has_prev || isLoading} 
            variant="outline"
            className="bg-gray-800 border-gray-700 hover:bg-gray-700"
          >
            Anterior
          </Button>
          <span className="">
            Página {pagination?.page || 1} de {pagination?.total_pages || 1} 
          </span>
          <Button
            onClick={handleNextPage}
            disabled={!pagination?.has_next || isLoading}
            variant="outline"
            className="bg-gray-800 border-gray-700 hover:bg-gray-700"
          >
            Próxima
          </Button>
        </div>

      </div>
    </main>
  );
}
