import { useEffect, useMemo, useState } from 'react'
import {
  AppBar,
  Box,
  Button,
  Chip,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  Toolbar,
  Typography,
} from '@mui/material'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Paper from '@mui/material/Paper'

type Prescription = {
  prescription_id: number
  patient_id: number
  drug_name: string
  arrived_at_clinic: string | null
  dispensed: boolean
  notes: string | null
}

type Patient = {
  patient_id: number
  national_id: number
  private_name: string
  last_name: string
  email: string | null
  location: string | null
  last_picked_up_date: string | null
  is_active: boolean
  prescriptions: Prescription[]
}

type SortKey = 'last_name' | 'private_name' | 'national_id'

const API_BASE_URL = 'http://127.0.0.1:8000'

const fallbackPatients: Patient[] = [
  {
    patient_id: 1,
    national_id: 123456789,
    private_name: 'Dana',
    last_name: 'Cohen',
    email: 'dana@example.com',
    location: 'Shelf A3',
    last_picked_up_date: '2026-03-15',
    is_active: true,
    prescriptions: [
      {
        prescription_id: 10,
        patient_id: 1,
        drug_name: 'Metformin',
        arrived_at_clinic: '2026-03-20',
        dispensed: false,
        notes: null,
      },
      {
        prescription_id: 11,
        patient_id: 1,
        drug_name: 'Atorvastatin',
        arrived_at_clinic: '2026-03-25',
        dispensed: true,
        notes: 'Nightly',
      },
    ],
  },
]

function App() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [sortKey, setSortKey] = useState<SortKey>('last_name')

  useEffect(() => {
    let cancelled = false

    async function loadPatients() {
      try {
        setLoading(true)
        setError(null)

        const res = await fetch(`${API_BASE_URL}/patients/`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)

        const data = (await res.json()) as Patient[]
        if (!cancelled) setPatients(data)
      } catch (e) {
        if (!cancelled) {
          setPatients(fallbackPatients)
          setError(
            'Could not reach the backend yet (showing example data). Once CORS is configured for the frontend dev server, this will load real patients.',
          )
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    void loadPatients()
    return () => {
      cancelled = true
    }
  }, [])

  const sortedPatients = useMemo(() => {
    const copy = [...patients]
    copy.sort((a, b) => {
      if (sortKey === 'national_id') return a.national_id - b.national_id
      return (a[sortKey] ?? '').localeCompare(b[sortKey] ?? '', undefined, {
        sensitivity: 'base',
      })
    })
    return copy
  }, [patients, sortKey])

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="sticky" elevation={1}>
        <Toolbar sx={{ gap: 1, flexWrap: 'wrap' }}>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Chrono
          </Typography>
          <Button color="inherit" disabled>
            Add new patient
          </Button>
          <Button color="inherit" disabled>
            Remove patient
          </Button>
          <Button color="inherit" disabled>
            Renewal of drugs
          </Button>
          <Button color="inherit" disabled>
            Probation dashboard
          </Button>
          <Button color="inherit" disabled>
            Add prescription
          </Button>
        </Toolbar>
      </AppBar>

      <Container sx={{ py: 3 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
          <Box>
            <Typography variant="h5" sx={{ mb: 0.5 }}>
              Patients
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Main welcome screen: list of patients, location, and their drugs.
            </Typography>
          </Box>

          <FormControl size="small" sx={{ minWidth: 260 }}>
            <InputLabel id="sort-by-label">Sort by</InputLabel>
            <Select
              labelId="sort-by-label"
              value={sortKey}
              label="Sort by"
              onChange={(e) => setSortKey(e.target.value as SortKey)}
            >
              <MenuItem value="last_name">Last name</MenuItem>
              <MenuItem value="private_name">First name</MenuItem>
              <MenuItem value="national_id">ID</MenuItem>
            </Select>
          </FormControl>
        </Stack>

        {error && (
          <Box sx={{ mb: 2 }}>
            <Chip color="warning" label={error} sx={{ height: 'auto', py: 1 }} />
          </Box>
        )}

        <TableContainer component={Paper} variant="outlined">
          <Table size="small" aria-label="patients table">
            <TableHead>
              <TableRow>
                <TableCell>Last name</TableCell>
                <TableCell>First name</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Last pickup</TableCell>
                <TableCell>Drugs</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6}>Loading…</TableCell>
                </TableRow>
              ) : sortedPatients.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6}>No patients yet.</TableCell>
                </TableRow>
              ) : (
                sortedPatients.map((p) => {
                  const drugNames = Array.from(
                    new Set((p.prescriptions ?? []).map((rx) => rx.drug_name).filter(Boolean)),
                  )
                  return (
                    <TableRow key={p.patient_id} hover>
                      <TableCell>{p.last_name}</TableCell>
                      <TableCell>{p.private_name}</TableCell>
                      <TableCell>{p.email ?? '—'}</TableCell>
                      <TableCell>{p.location ?? '—'}</TableCell>
                      <TableCell>{p.last_picked_up_date ?? '—'}</TableCell>
                      <TableCell sx={{ minWidth: 220 }}>
                        <FormControl size="small" fullWidth>
                          <InputLabel id={`drugs-label-${p.patient_id}`}>Drugs</InputLabel>
                          <Select
                            labelId={`drugs-label-${p.patient_id}`}
                            label="Drugs"
                            value=""
                            displayEmpty
                            renderValue={() =>
                              drugNames.length ? `${drugNames.length} drugs` : 'No drugs'
                            }
                          >
                            {drugNames.length === 0 ? (
                              <MenuItem disabled value="">
                                No prescriptions
                              </MenuItem>
                            ) : (
                              drugNames.map((name) => (
                                <MenuItem key={name} value={name}>
                                  {name}
                                </MenuItem>
                              ))
                            )}
                          </Select>
                        </FormControl>
                      </TableCell>
                    </TableRow>
                  )
                })
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Container>
    </Box>
  )
}

export default App
