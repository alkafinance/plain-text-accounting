export interface Ledger {
  accounts: Account[];
  commodities: Commodity[];
  date: string;
  id: string;
  tags: any[];
  title: string;
  transactions: Transaction[];
}

export interface Account {
  closeDate: any;
  id: string;
  openDate: string;
  path: string;
}

export interface Commodity {
  id: string;
  name: any;
  unit: string;
}

export interface Transaction {
  date: string;
  flag: string;
  id: string;
  links: any[];
  narration: string;
  payee?: string;
  postings: Posting[];
  tagNames: string[];
}

export interface Posting {
  accountPath: string;
  amount: Amount;
  flag: any;
  id: string;
}

export interface Amount {
  quantity: number;
  unit: string;
}
