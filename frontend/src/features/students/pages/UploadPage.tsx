import React, { useState } from "react";
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  AppBar,
  Toolbar,
  IconButton,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import DashboardIcon from "@mui/icons-material/Dashboard";
import LogoutIcon from "@mui/icons-material/Logout";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../../../store/store";
import { logout } from "../../../store/slices/authSlice";
import axios from "axios";

interface ValidationError {
  row: number;
  field: string;
  value: string | number;
  message: string;
}

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<ValidationError[]>([]);
  const [success, setSuccess] = useState<string | null>(null);
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setErrors([]);
      setSuccess(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Por favor seleccione un archivo");
      return;
    }

    setLoading(true);
    setErrors([]);
    setSuccess(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("/students/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.data.success) {
        setSuccess(response.data.message || "Archivo procesado exitosamente");
        setFile(null);
        // Reset file input
        const fileInput = document.getElementById(
          "file-upload"
        ) as HTMLInputElement;
        if (fileInput) fileInput.value = "";
      }
    } catch (error: any) {
      if (error.response?.data?.errors) {
        setErrors(error.response.data.errors);
      } else {
        setErrors([
          {
            row: 0,
            field: "file",
            value: "",
            message:
              error.response?.data?.error || "Error al procesar el archivo",
          },
        ]);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Carga de Estudiantes
          </Typography>
          <IconButton color="inherit" onClick={() => navigate("/dashboard")}>
            <DashboardIcon />
          </IconButton>
          <IconButton color="inherit" onClick={handleLogout}>
            <LogoutIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Cargar Archivo de Estudiantes
          </Typography>
          <Typography variant="body1" color="textSecondary" paragraph>
            Seleccione un archivo Excel (.xlsx, .xls) o CSV con los datos de los
            estudiantes. El archivo debe contener las columnas:
            nombre_estudiante, anio_inicio, NUE, promedio_actual,
            promedio_graduacion, estado.
          </Typography>

          <Box sx={{ mt: 3, mb: 3 }}>
            <input
              accept=".xlsx,.xls,.csv"
              style={{ display: "none" }}
              id="file-upload"
              type="file"
              onChange={handleFileChange}
            />
            <label htmlFor="file-upload">
              <Button
                variant="outlined"
                component="span"
                startIcon={<UploadFileIcon />}
                disabled={loading}
              >
                Seleccionar Archivo
              </Button>
            </label>
            {file && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                Archivo seleccionado: {file.name}
              </Typography>
            )}
          </Box>

          <Button
            variant="contained"
            onClick={handleUpload}
            disabled={!file || loading}
            startIcon={
              loading ? <CircularProgress size={20} /> : <UploadFileIcon />
            }
            sx={{ mb: 3 }}
          >
            {loading ? "Procesando..." : "Subir Archivo"}
          </Button>

          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              {success}
            </Alert>
          )}

          {errors.length > 0 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" color="error" gutterBottom>
                Errores de Validación ({errors.length})
              </Typography>
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>
                        <strong>Fila</strong>
                      </TableCell>
                      <TableCell>
                        <strong>Campo</strong>
                      </TableCell>
                      <TableCell>
                        <strong>Valor</strong>
                      </TableCell>
                      <TableCell>
                        <strong>Mensaje</strong>
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {errors.map((error, index) => (
                      <TableRow key={index}>
                        <TableCell>{error.row}</TableCell>
                        <TableCell>{error.field}</TableCell>
                        <TableCell>{String(error.value)}</TableCell>
                        <TableCell>{error.message}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          )}
        </Paper>
      </Container>
    </>
  );
};

export default UploadPage;
