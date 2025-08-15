// --- DEFINIÇÕES DE TIPOS COMPARTILHADAS ---
export type CovidData = {
  id: number;
  country: string;
  cases: number;
  deaths: number;
  report_date: string;
}

export type PaginationInfo = {
  page: number;
  per_page: number;
  total_pages: number;
  total_items: number;
  has_next: boolean;
  has_prev:boolean;
}

export type PaginatedResponse = {
    data: CovidData[];
    pagination: PaginationInfo;
}

export type CountrySummary = {
    country: string;
    total_cases: number;
    total_deaths: number;
}


// --- CONFIGURAÇÃO BASE DA API ---
const API_BASE_URL = "http://localhost:5001/api"


// --- FUNÇÕES DE FETCH ---

/**
 * Busca a lista de todos os países disponíveis.
 */
export async function getCountries(): Promise<string[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/countries`);
        if (!response.ok) {
            throw new Error("A resposta da rede não foi \"ok\".");
        }
        return response.json();
    } catch (error) {
        console.error("Falha ao buscar países:", error);
        return [];
    }
}


/**
 * Busca uma página de dados da COVID, com filtros opcionais.
 * @param page - O número da página a ser buscada.
 * @param country - O país para filtrar (ou 'all' para nenhum filtro).
 */
export async function getPaginatedData(page: number, country: string): Promise<PaginatedResponse> {
    const params = new URLSearchParams();
    params.append("page", page.toString());
    if (country !== "all") {
        params.append("country", country);
    }

    try {
        const response = await fetch(`${API_BASE_URL}/data?${params.toString()}`);
        if (!response.ok) {
            throw new Error("A resposta da rede não foi \"ok\".");
        }
        return response.json();
    } catch (error) {
        console.error("Falha ao buscar dados paginados:", error);

        return {
            data: [],
            pagination: {
                page: 1,
                per_page: 20,
                total_pages: 1,
                total_items: 0,
                has_next: false,
                has_prev: false,
            },
        };
    }
}

/**
 * Busca os dados de resumo agregado por país para o gráfico.
 */
export async function getCountrySummary(): Promise<CountrySummary[]> {
    try {
        const response = await fetch(`${API_BASE_URL}/summary/by-country`);
        if (!response.ok) {
            throw new Error("A resposta da rede não foi \"ok\".");
        }
        return response.json();
    } catch (error) {
        console.error("Falha ao buscar o resumo por país:", error);
        return[];
    }
}