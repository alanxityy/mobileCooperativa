import React, { useState, useEffect } from 'react';
import api from './src/services/api';
import { 
  View, Text, Image, Modal, StyleSheet, TextInput, 
  TouchableOpacity, ScrollView, SafeAreaView, StatusBar, 
  ActivityIndicator, Dimensions
} from 'react-native';
import { 
  format, startOfMonth, endOfMonth, startOfWeek, 
  endOfWeek, eachDayOfInterval, isSameMonth,
  addMonths, subMonths 
} from 'date-fns';
import { ptBR } from 'date-fns/locale';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authService } from './src/services/authService';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState(null);
  const [profileData, setProfileData] = useState(null);

  const [mesVisivel, setMesVisivel] = useState(new Date());
  const [notas, setNotas] = useState({});
  const [modalVisivel, setModalVisivel] = useState(false);
  const [diaSelecionado, setDiaSelecionado] = useState(null);
  const [textoNota, setTextoNota] = useState('');

  useEffect(() => {
    const verificarSessao = async () => {
      // store token
      const tokenSalvo = localStorage.getItem('userToken');
      const perfilSalvo = localStorage.getItem('userData');

      if (tokenSalvo && perfilSalvo) {
        setToken(tokenSalvo);
        setProfileData(JSON.parse(perfilSalvo));
        setIsLoggedIn(true);
        carregarNotas(JSON.parse(perfilSalvo).username || user);
      }
    };
    verificarSessao();
  }, []);

  useEffect(() => {
    if (isLoggedIn && token) {
      const buscarNotasDoServidor = async () => {
        try {
          const response = await api.get('/api/notas/', {
            headers: { Authorization: `Bearer ${token}` }
          });

          const mapaNotas = {};
          response.data.forEach(nota => {
            mapaNotas[nota.data_br] = nota.texto;
          });

          setNotas(mapaNotas);
        } catch (error) {
          console.error("Erro ao buscar notas:");
        }
      };
      buscarNotasDoServidor();
    }
  }, [isLoggedIn, token]);

  const carregarNotas = async (username) => {
    const salvas = await AsyncStorage.getItem(`notas_cal_${username}`);
    if (salvas) setNotas(JSON.parse(salvas));
  };

  const handleLogin = async () => {
    if (!user || !pass) {
      alert("Por favor, preencha todos os campos.");
      return;
    }
    setLoading(true);
    try {
      const result = await authService.login(user, pass);
      if (result.success) {
        const accessToken = result.data.access; 
        const profiles = await authService.getPerfis(accessToken);
        if (profiles) {
          const meuPerfil = profiles.find(p => p.username?.toLowerCase() === user.toLowerCase()) || profiles[0];
          
          setToken(accessToken);
          setProfileData(meuPerfil);
          setIsLoggedIn(true);

          localStorage.setItem('userToken', accessToken);
          localStorage.setItem('userData', JSON.stringify(meuPerfil));
          localStorage.setItem('loginTimestamp', new Date().getTime().toString());
          carregarNotas(meuPerfil.username);
        }
      } else {
        alert("Erro: " + result.message);
      }
    } catch (error) {
      alert("Ocorreu um erro ao processar o login");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('userToken');
  localStorage.removeItem('userData');
  localStorage.removeItem('loginTimestamp');

    setToken(null);
    setProfileData(null);
    setIsLoggedIn(false);
    setNotas({});
    setUser('');
    setPass('');
  };

  const salvarNota = async () => {
    const dataBR = format(diaSelecionado, 'dd/MM/yyyy');
    const novasNotas = { ...notas };

    if (textoNota.trim() === "") {
      delete novasNotas[dataBR];
    } else {
      novasNotas[dataBR] = textoNota;
    }

    try {
      await api.post('/api/notas/', {
        data_br: dataBR,
        texto: textoNota
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

    } catch (error) {
      console.warn("Erro ao sincronizar com servidor, salvo apenas localmente.");
    }

    const chaveStorage = `notas_cal_${profileData?.username || user}`;
    await AsyncStorage.setItem(chaveStorage, JSON.stringify(novasNotas));

    setNotas(novasNotas);
    setModalVisivel(false);
  };

  const renderCalendario = () => {
  const inicioMes = startOfMonth(mesVisivel);
  const fimMes = endOfMonth(mesVisivel);
  const dias = eachDayOfInterval({
    start: startOfWeek(inicioMes),
    end: endOfWeek(fimMes),
  });

  return (
    <View style={styles.calWrapper}>
      <View style={styles.calHeaderNav}>
        <TouchableOpacity onPress={() => setMesVisivel(subMonths(mesVisivel, 1))}>
          <Text style={styles.seta}>◀</Text>
        </TouchableOpacity>
        <Text style={styles.calTitleText}>
          {format(mesVisivel, "MMMM 'de' yyyy", { locale: ptBR })}
        </Text>
        <TouchableOpacity onPress={() => setMesVisivel(addMonths(mesVisivel, 1))}>
          <Text style={styles.seta}>▶</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.gradeCalendario}>
        {['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'].map(d => (
          <Text key={d} style={styles.diaSemanaLabel}>{d}</Text>
        ))}
        
        {dias.map((data, i) => {
          const dataBR = format(data, 'dd/MM/yyyy');
          const temNota = notas[dataBR]; 
          const foraDoMes = !isSameMonth(data, mesVisivel); 

          return (
            <TouchableOpacity 
              key={i} 
              style={[
                styles.diaBotao, 
                temNota && styles.diaComNota, 
                foraDoMes && { opacity: 0.3 }
              ]}
              onPress={() => {
                setDiaSelecionado(data);
                setTextoNota(notas[dataBR] || '');
                setModalVisivel(true);
              }}
            >
              <Text style={styles.diaTexto}>{format(data, 'd')}</Text>
              {temNota && <View style={styles.marcadorNota} />}
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
};

  if (isLoggedIn) {
    const userPhotoSource = profileData?.foto 
      ? { uri: profileData.foto.startsWith('http') ? profileData.foto : `${api.defaults.baseURL.split('/api')[0]}${profileData.foto}` }
      : null;

    return (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="light-content" />
        <View style={styles.header}>
          <View style={styles.logoArea}>
            <Image
              source={require("./assets/logo_suzanapolis.png")}
              style={styles.logoImage}
            />
          </View>
          <View style={styles.navBar}>
            <View style={styles.navLinksContainer}>
              <Text style={styles.navItem}>Dashboard</Text>
              <Text style={styles.navItem}>Materiais</Text>
              <Text style={styles.navItem}>Caixa</Text>
            </View>

            <TouchableOpacity style={styles.navRight} onPress={handleLogout}>
              <Text style={styles.navLogout}>Sair</Text>
            </TouchableOpacity>
          </View>
        </View>

        <ScrollView
          style={styles.dashboardContent}
          contentContainerStyle={{ paddingBottom: 40 }}
        >
          <Text style={styles.mainTitle}>Dashboard</Text>
          <Text style={styles.subTitleText}>
            Bem-vindo, {profileData?.username || user}.
          </Text>

          <View style={styles.card}>
            <Text style={styles.cardHeader}>Seu perfil</Text>
            <View style={styles.profileBox}>
              <View style={styles.avatarCircle}>
                {userPhotoSource ? (
                  <Image
                    source={userPhotoSource}
                    style={{ width: 60, height: 60 }}
                  />
                ) : (
                  <Text style={{ fontSize: 24 }}>👤</Text>
                )}
              </View>
              <View>
                <Text style={styles.profileName}>
                  {profileData?.username || user}
                </Text>
                <Text style={styles.profileStatus}>
                  ● {profileData?.cargo || "Membro"}
                </Text>
              </View>
            </View>
          </View>

          <View style={[styles.card, { marginTop: 20 }]}>
            <Text style={styles.cardHeader}>Calendário de Notas</Text>
            {renderCalendario()}
          </View>
        </ScrollView>

        <Modal visible={modalVisivel} transparent animationType="fade">
          <View style={styles.modalOverlay}>
            <View style={styles.modalContent}>
              <Text style={styles.modalTitle}>
                Nota para{" "}
                {diaSelecionado && format(diaSelecionado, "dd/MM/yyyy")}
              </Text>
              <TextInput
                style={styles.inputNota}
                multiline
                value={textoNota}
                onChangeText={setTextoNota}
                placeholder="Escreva algo..."
              />
              <View style={styles.modalBotoes}>
                <TouchableOpacity
                  onPress={() => setModalVisivel(false)}
                  style={[styles.btnModal, { backgroundColor: "#666" }]}
                >
                  <Text style={{ color: "#fff" }}>Cancelar</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={salvarNota} style={styles.btnModal}>
                  <Text style={{ color: "#fff" }}>Salvar</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </Modal>
      </SafeAreaView>
    );
  }

  // Tela de Login 
  return (
    <View style={styles.loginContainer}>
      <Text style={styles.loginTitle}>Cooperativa Login</Text>
      <View style={styles.form}>
        <TextInput style={styles.input} placeholder="Usuário" placeholderTextColor="#999" value={user} onChangeText={setUser} autoCapitalize="none" />
        <TextInput style={styles.input} placeholder="Senha" placeholderTextColor="#999" secureTextEntry value={pass} onChangeText={setPass} />
        <TouchableOpacity style={styles.button} onPress={handleLogin} disabled={loading}>
          {loading ? <ActivityIndicator color="white" /> : <Text style={styles.buttonText}>ENTRAR</Text>}
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f0f2f5' },
  header: { backgroundColor: '#0033A0' },
  logoArea: { height: 60, justifyContent: 'center', alignItems: 'center' },
  logoImage: { height: 50, width: '100%', resizeMode: 'contain' },
  logoText: { color: 'white', fontSize: 20, fontWeight: 'bold', letterSpacing: 2 },
  navBar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'flex-start', backgroundColor: '#02329b', padding: 12, borderTopWidth: 3, borderTopColor: '#FFD700', paddingHorizontal: 20, width: '100%' },
  navLinksContainer: { flexDirection: 'row', alignItems: 'center', gap: 20 },
  navItem: { color: 'white', fontSize: 14, fontWeight: '500' },
  navItemHover: { backgroundColor: '#ffcc00', color: '#0033a0' },
  navRight: { marginLeft: 'auto' },
  navLogout: { color: 'white', fontWeight: 'bold' },
  dashboardContent: { padding: 20 },
  mainTitle: { fontSize: 24, fontWeight: 'bold', color: '#1a1a1a' },
  subTitleText: { fontSize: 14, color: '#666', marginBottom: 20 },
  card: { backgroundColor: 'white', borderRadius: 10, padding: 15, elevation: 3 },
  cardHeader: { fontSize: 16, fontWeight: 'bold', marginBottom: 10, borderBottomWidth: 1, borderBottomColor: '#eee', paddingBottom: 5 },
  profileBox: { flexDirection: 'row', alignItems: 'center' },
  avatarCircle: { width: 60, height: 60, borderRadius: 30, backgroundColor: '#eee', justifyContent: 'center', alignItems: 'center', marginRight: 15, overflow: 'hidden' },
  profileName: { fontSize: 16, fontWeight: 'bold' },
  profileStatus: { color: '#28a745', fontSize: 12 },

  // Calendário
  calWrapper: { marginTop: 10 },
  calHeaderNav: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 },
  calTitleText: { fontSize: 16, fontWeight: 'bold', textTransform: 'capitalize' },
  seta: { fontSize: 18, color: '#0033A0', padding: 5 },
  gradeCalendario: { flexDirection: 'row', flexWrap: 'wrap' },
  diaSemanaLabel: { width: '14.28%', textAlign: 'center', fontSize: 12, color: '#999', marginBottom: 5 },
  diaBotao: { width: '14.28%', height: 45, justifyContent: 'center', alignItems: 'center', borderWidth: 0.2, borderColor: '#eee' },
  diaTexto: { fontSize: 14 },
  diaComNota: { backgroundColor: '#fff7cc' },
  marcadorNota: { width: 4, height: 4, backgroundColor: '#FFD700', borderRadius: 2, marginTop: 2 },

  // Modal
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', alignItems: 'center' },
  modalContent: { backgroundColor: 'white', width: '85%', borderRadius: 15, padding: 20 },
  modalTitle: { fontSize: 16, fontWeight: 'bold' },
  inputNota: { borderBottomWidth: 1, borderColor: '#ddd', marginVertical: 15, height: 80, textAlignVertical: 'top' },
  modalBotoes: { flexDirection: 'row', justifyContent: 'space-between' },
  btnModal: { padding: 10, borderRadius: 8, backgroundColor: '#0033A0', width: '48%', alignItems: 'center' },

  // Login
  loginContainer: { flex: 1, backgroundColor: '#121212', justifyContent: 'center', padding: 30 },
  loginTitle: { color: 'white', fontSize: 26, textAlign: 'center', marginBottom: 30 },
  input: { backgroundColor: '#1e1e1e', color: 'white', padding: 15, borderRadius: 8, marginBottom: 15 },
  button: { backgroundColor: '#0056b3', padding: 15, borderRadius: 8, alignItems: 'center' },
  buttonText: { color: 'white', fontWeight: 'bold' }
});