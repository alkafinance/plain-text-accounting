export interface Ledger {
  version: 'standard-1'
  accounts: Account[];
  commodities: Commodity[];
  transactions: Transaction[];
  prices: Price[]
}

type Unit = string
type ISODate = string
type ISODateTime = string


// Copied from Standard.d.ts

export type ConnectionStatus = 'connected' | 'disconnected' | 'error'

export interface Connection {
  lastSuccessfulRefresh?: ISODateTime | null
  status: ConnectionStatus
  name?: string | null
  institution?: {
    name: string
    logoUrl: string
    url: string
  }
  /**
   * Whether we should hide the connection from user interface because
   * it's really an implementation detail. Only applies to Yodlee.User for now
   */
  hidden?: boolean
  removed?: boolean
}

/** Deprecated. Used AccountTypePrefix */
export type StatementType = AccountTypePrefix

export type AccountTypePrefix = 'balance_sheet' | 'income_statement' | 'other'
export type AccountType =
  | 'balance_sheet'
  | 'balance_sheet/asset'
  | 'balance_sheet/liability'
  | 'balance_sheet/equity'
  | 'income_statement' // Default
  | 'income_statement/income'
  | 'income_statement/expense'
  | 'other'

export type AccountSubtypePrefix =
  | 'misc'
export type AccountSubtype =
  // TODO: Map plaid and yodlee ones to these guys
  | 'cash'
  | 'checking'
  | 'savings'
  | 'credit_card'
  | 'mortgage'
  | 'accounts_receivable'
  | 'expense/fees'
  // Normally maps to type:other, but not necessarily.
  | 'misc/initial_balance'
  | 'misc/transfer'
  | 'misc/balance_assignment'
  | 'misc/reconcilation_error' // Equivalent to balance assertion
  | 'misc/trading' // https://www.mathstat.dal.ca/~selinger/accounting/tutorial.html
  | 'misc/uncategorized'

/** For inspiration, see Plaid.SecurityType */
export type CommodityType =
  | 'currency'
  | 'stock'
  | 'crypto'
  // real_estate, etc.

/**
 * Holding is really nothing but a posting and we may not actually need it at all
 * See https://docs.google.com/document/d/1qPdNXaz5zuDQ8M9uoZFyyFis7hA0G55BEfhWhrVBsfc/edit#heading=h.n5ispaok8sog
 * However many data vendors end up giving this and until we have a better way
 * of representing it we'll keep it in the standard core. Though we should
 * make this field not directly editable by the user, and only used at runtime
 * by the providers
 */
export interface _Holding extends Amount {
  /** Per unit, not total. Informational, not used in accounting equation */
  costBasis?: Amount | null
  /** Per unit, not total. Informational, not used in accounting equation */
  lastQuote?: Amount | null
  lastQuoteDate?: ISODate | null
}

export interface Account {
  /** e.g. `Chase Checking` */
  name: string
  type?: AccountType
  subtype?: AccountSubtype

  lastFour?: string | null
  institutionName?: string | null
  /** ISO country code ideally, but really could be anything... */
  countryCode?: string | null
  openDate?: ISODate | null
  closeDate?: ISODate | null
  notes?: string | null
  defaultUnit?: Unit | null
  /** https://en.wikipedia.org/wiki/Cash_and_cash_equivalents#:~:text=Cash%20and%20cash%20equivalents%20(CCE,into%20a%20known%20cash%20amount%22. */
  liquidity?: string | null
  // Add me when I'm useful
  // currentBalance?: Amount | null
  // availableBalance?: Amount | null
  // limitBalance?: Amount | null
  balance?: Amount | null
  /**
   * Should not be edited by the user
   * When present, the `balance` field above should be completely informational
   * and not factor into the accounting equation
   */
  readonly holdings?: _Holding[] | null

  // Historical balance should be
  // implemented as balance assertions
  removed?: boolean
}

export interface Transaction {
  // TODO: Move `date` and `flags` to be optional fields on postings rather
  // than on transactions
  // TODO: Evaluate using different dates for `is` posting vs `bs` posting
  // as a easy way to do accrual accounting? (think house utilities)
  date: ISODateTime | ISODate
  flags?: Flags

  /**
   * Aka Merchant | Customer | Vendor
   * Often time same as the simpleDescription field. In particular this is a field
   * we can depend on to render custom icons for each transaction (e.g. Walmart icon)
   */
  payee?: string

  /**
   * Should be exactly as it appears on user's bank statement.
   * payee | merchant | name https://hledger.org/journal.html#payee-and-note
   */
  description: string

  /**
   *
   * Provider's best guess attempt at an easy-to-understand, plain-language
   * transaction description derived from original, abbreviated and, sometimes
   * cryptic, transaction description
   * https://developer.yodlee.com/docs/api/1.1/Transaction_Data_Enrichment
   */
  simpleDescription?: string
  notes?: string | null
  postingsMap?: Record<string, Posting>

  /** Label Name -> enabled */
  labelsMap?: Record<string, boolean>

  /** https://support.plaid.com/hc/en-us/articles/360008271814-Pending-transaction-overview */
  pendingTransactionExternalId?: string | null

  // TODO: Build abstraction to be able to express this in a
  // generic way for all objects
  removed?: boolean
}

export interface Flags {
  pending?: boolean | null
  followUp?: boolean | null
  confirmed?: boolean | null
  // Hardly used
  cancelled?: boolean | null
  // Can this be considered a transfer?
  transfer?: boolean | null
}


export interface Posting {
  date?: ISODateTime | ISODate
  /** Do not use for now */
  flags?: Flags

  // This should technically be called `acountId` however
  // that would conflict with Raw.Posting, oh well...

  // TODO: Should we turn these into an actual
  // `Account` field?
  /** Maps to accountId?: Id.acct */
  accountExternalId?: string
  /** Chase Checking */
  accountName?: string | null
  accountType?: AccountType
  accountSubtype?: AccountSubtype

  memo?: string | null
  amount: Amount
  /** Balance assignment */
  balance?: Amount

  // Should we actually support both total and unit cost? Is that worth
  // the complexity?

  /**
   * Comment out as price ought to be inferred. However, which specific
   * posting would have inferred price? Now that's the question
   */
  // price?: {amount: Amount; type: 'unit' | 'total'} | null

  /**
   * See https://share.getcloudapp.com/ApukLmdx
   * Mainly useful for lot-tracking and holding information.
   * Would be inferred unless otherwise explicitly stated.
   * */
  cost?: {
    amount: Amount
    type: 'unit' | 'total'
    date?: ISODate
    label?: string
  } | null

  // TODO: Represent balance assignments / assertions
  // type?: 'normal' | 'assignment' | 'assertion'

  /** Posting level custom fields */
  custom?: Record<string, any>
}

// TODO: -- Add price / commodities support ---
/**
 * USD:CAD = 1.32
 * [base]:[target] = [rate]
 */
export interface Price {
  /** `USD` */
  baseUnit: string

  /** 1.32 CAD */
  quote: Amount
  // /** `CAD` */
  // targetUnit: string
  // /** `1.32` */
  // rate: number
  /** Assuming closing price of the day */
  date: ISODate
}

export interface Commodity {
  /** symbol. `USD` */
  unit: string
  /** `US Dollar` */
  name?: string
  type?: CommodityType | null
  description?: string
  exponent?: number | null
}

 interface Amount {
  unit: Unit
  quantity: number
}

