import React, { useEffect, useState } from "react";
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Card,
  CardContent,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import LogoutIcon from "@mui/icons-material/Logout";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../../../store/store";
import { logout } from "../../../store/slices/authSlice";
import axios from "axios";

interface Student {
  id: number;
  nombre_estudiante: string;
  nue: number;
  anio_inicio: number;
  promedio_actual: number | null;
  promedio_graduacion: number | null;
  graduado: boolean;
}

interface Statistics {
  total: number;
  active: number;
  graduated: number;
  avg_by_status: Array<{
    graduado: number;
    avg_promedio: number;
  }>;
  by_year: Array<{
    anio_inicio: number;
    count: number;
  }>;
}

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

const DashboardPage: React.FC = () => {
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsResponse, studentsResponse] = await Promise.all([
        axios.get("/dashboard/statistics"),
        axios.get("/dashboard/students"),
      ]);
      setStatistics(statsResponse.data);
      setStudents(studentsResponse.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  const statusData = statistics
    ? [
        { name: "Activos", value: statistics.active },
        { name: "Graduados", value: statistics.graduated },
      ]
    : [];

  const yearData = statistics?.by_year.slice(0, 10) || [];

  const avgData =
    statistics?.avg_by_status
      .map((item) => {
        const avgValue =
          item.avg_promedio != null ? parseFloat(String(item.avg_promedio)) : 0;
        return {
          name: item.graduado ? "Graduados" : "Activos",
          promedio: isNaN(avgValue) ? 0 : parseFloat(avgValue.toFixed(2)),
        };
      })
      .filter((item) => item.promedio > 0) || [];

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Dashboard - Sistema de Educación
          </Typography>
          <IconButton color="inherit" onClick={() => navigate("/upload")}>
            <UploadFileIcon />
          </IconButton>
          <IconButton color="inherit" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {loading ? (
          <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight="400px"
          >
            <Typography>Cargando datos...</Typography>
          </Box>
        ) : (
          <>
            <Grid container spacing={3}>
              {/* Summary Cards */}
              <Grid item xs={12} sm={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Total Estudiantes
                    </Typography>
                    <Typography variant="h4">
                      {statistics?.total || 0}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Estudiantes Activos
                    </Typography>
                    <Typography variant="h4" color="primary">
                      {statistics?.active || 0}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Estudiantes Graduados
                    </Typography>
                    <Typography variant="h4" color="success.main">
                      {statistics?.graduated || 0}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              {/* Pie Chart - Status Distribution */}
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Distribución por Estado
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={statusData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) =>
                          `${name} ${(percent * 100).toFixed(0)}%`
                        }
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {statusData.map((entry, index) => (
                          <Cell
                            key={`cell-${index}`}
                            fill={COLORS[index % COLORS.length]}
                          />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </Paper>
              </Grid>

              {/* Bar Chart - Students by Year */}
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Estudiantes por Año de Inicio
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={yearData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="anio_inicio" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="count" fill="#8884d8" name="Estudiantes" />
                    </BarChart>
                  </ResponsiveContainer>
                </Paper>
              </Grid>

              {/* Line Chart - Average by Status */}
              <Grid item xs={12}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Promedio por Estado
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={avgData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis domain={[0, 10]} />
                      <Tooltip />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="promedio"
                        stroke="#8884d8"
                        name="Promedio"
                        strokeWidth={2}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Paper>
              </Grid>
            </Grid>
          </>
        )}
      </Container>
    </>
  );
};

export default DashboardPage;
