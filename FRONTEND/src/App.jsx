import { useEffect, useState } from 'react'
import './App.css'
import logo from './assets/logo_bp.png'
import facebookIcon from './assets/facebook.svg'
import instagramIcon from './assets/instagram.svg'
import twitterIcon from './assets/twitter.svg'
import youtubeIcon from './assets/youtube.svg'

// Variables d'environnement avec Vite
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const PREDICT_ENDPOINT = import.meta.env.VITE_PREDICT_ENDPOINT || '/predict';


function App() {

  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    polyuria: '',
    polydipsia: '',
    sudden_weight_loss: '',
    weakness: '',
    polyphagia: '',
    genital_thrush: '',
    visual_blurring: '',
    itching: '',
    irritability: '',
    delayed_healing: '',
    partial_paresis: '',
    muscle_stiffness: '',
    alopecia: '',
    obesity: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };


  const handleSubmitForm = async (e) => {
    e.preventDefault();
    
    // Validation : vérifier que tous les champs sont remplis
    const requiredFields = Object.keys(formData);
    const emptyFields = requiredFields.filter(field => !formData[field]);
    
    if (emptyFields.length > 0) {
      setError('Veuillez remplir tous les champs du formulaire.');
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      // Convertir l'âge en nombre entier
      const dataToSend = {
        ...formData,
        age: parseInt(formData.age)
      };

      console.log('Données envoyées:', dataToSend);

      const response = await fetch(`${API_URL}${PREDICT_ENDPOINT}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSend),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const result = await response.json();
      console.log('Réponse reçue:', result);
      setPrediction(result);

    } catch (err) {
      console.error('Erreur lors de la requête:', err);
      setError(`Erreur lors de la prédiction: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>

      <header>
        <div className='header_band'>
          <nav>
            {/* Ligne du haut : Logo + Titres + Burger */}
            <div className="nav-top">
              <a href='/' className="logo-link">
                <img src={logo} className='logo_bp' alt="Logo Centre Hospitalier" />
              </a>
              <div className="nav-titles">
                <h1>CENTRE HOSPITALIER</h1>
                <h2>Felix Guichard</h2>
              </div>
              
              {/* Bouton Burger */}
              <button 
                className={`burger-menu ${isMenuOpen ? 'open' : ''}`}
                onClick={toggleMenu}
                aria-label="Menu de navigation"
              >
                <span className="burger-line"></span>
                <span className="burger-line"></span>
                <span className="burger-line"></span>
              </button>
            </div>
            
            {/*liens de navigation */}
            <div className={`nav-links ${isMenuOpen ? 'open' : ''}`}>
              <a href="/rendez-vous" onClick={() => setIsMenuOpen(false)}>Demander un rendez-vous</a>
              <a href="/professionnels" onClick={() => setIsMenuOpen(false)}>Professionnel de santé</a>
              <a href="/parcours" onClick={() => setIsMenuOpen(false)}>Voir votre parcours Santé +</a>
              <a href="/about" onClick={() => setIsMenuOpen(false)}>À propos</a>
            </div>
          </nav>
        </div>
      </header>

      <section>
        <form onSubmit={handleSubmitForm} className="patient-form">
          <h2>Évaluation des Symptômes du Diabète</h2>
          
          {/* Champ âge */}
          <div className="form-group">
            <label htmlFor="age">Âge :</label>
            <input
              type="number"
              id="age"
              name="age"
              value={formData.age}
              onChange={handleChange}
              min="0"
              max="120"
              required
            />
          </div>

          {/* Genre */}
          <div className="form-group">
            <label>Genre :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="gender"
                  value="Male"
                  checked={formData.gender === 'Male'}
                  onChange={handleChange}
                />
                Homme
              </label>
              <label>
                <input
                  type="radio"
                  name="gender"
                  value="Female"
                  checked={formData.gender === 'Female'}
                  onChange={handleChange}
                />
                Femme
              </label>
            </div>
          </div>

          {/* Polyurie */}
          <div className="form-group">
            <label>Polyurie (miction excessive) :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="polyuria"
                  value="Yes"
                  checked={formData.polyuria === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="polyuria"
                  value="No"
                  checked={formData.polyuria === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Polydipsie */}
          <div className="form-group">
            <label>Polydipsie (soif excessive) :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="polydipsia"
                  value="Yes"
                  checked={formData.polydipsia === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="polydipsia"
                  value="No"
                  checked={formData.polydipsia === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Perte de poids soudaine */}
          <div className="form-group">
            <label>Perte de poids soudaine :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="sudden_weight_loss"
                  value="Yes"
                  checked={formData.sudden_weight_loss === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="sudden_weight_loss"
                  value="No"
                  checked={formData.sudden_weight_loss === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Faiblesse */}
          <div className="form-group">
            <label>Faiblesse :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="weakness"
                  value="Yes"
                  checked={formData.weakness === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="weakness"
                  value="No"
                  checked={formData.weakness === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Polyphagie */}
          <div className="form-group">
            <label>Polyphagie (faim excessive) :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="polyphagia"
                  value="Yes"
                  checked={formData.polyphagia === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="polyphagia"
                  value="No"
                  checked={formData.polyphagia === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Candidose génitale */}
          <div className="form-group">
            <label>Candidose génitale :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="genital_thrush"
                  value="Yes"
                  checked={formData.genital_thrush === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="genital_thrush"
                  value="No"
                  checked={formData.genital_thrush === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Vision floue */}
          <div className="form-group">
            <label>Vision floue :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="visual_blurring"
                  value="Yes"
                  checked={formData.visual_blurring === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="visual_blurring"
                  value="No"
                  checked={formData.visual_blurring === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Démangeaisons */}
          <div className="form-group">
            <label>Démangeaisons :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="itching"
                  value="Yes"
                  checked={formData.itching === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="itching"
                  value="No"
                  checked={formData.itching === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Irritabilité */}
          <div className="form-group">
            <label>Irritabilité :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="irritability"
                  value="Yes"
                  checked={formData.irritability === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="irritability"
                  value="No"
                  checked={formData.irritability === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Cicatrisation retardée */}
          <div className="form-group">
            <label>Cicatrisation retardée :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="delayed_healing"
                  value="Yes"
                  checked={formData.delayed_healing === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="delayed_healing"
                  value="No"
                  checked={formData.delayed_healing === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Parésie partielle */}
          <div className="form-group">
            <label>Parésie partielle :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="partial_paresis"
                  value="Yes"
                  checked={formData.partial_paresis === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="partial_paresis"
                  value="No"
                  checked={formData.partial_paresis === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Raideur musculaire */}
          <div className="form-group">
            <label>Raideur musculaire :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="muscle_stiffness"
                  value="Yes"
                  checked={formData.muscle_stiffness === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="muscle_stiffness"
                  value="No"
                  checked={formData.muscle_stiffness === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Alopécie */}
          <div className="form-group">
            <label>Alopécie (perte de cheveux) :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="alopecia"
                  value="Yes"
                  checked={formData.alopecia === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="alopecia"
                  value="No"
                  checked={formData.alopecia === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          {/* Obésité */}
          <div className="form-group">
            <label>Obésité :</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  name="obesity"
                  value="Yes"
                  checked={formData.obesity === 'Yes'}
                  onChange={handleChange}
                />
                Oui
              </label>
              <label>
                <input
                  type="radio"
                  name="obesity"
                  value="No"
                  checked={formData.obesity === 'No'}
                  onChange={handleChange}
                />
                Non
              </label>
            </div>
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Analyse en cours...' : 'Évaluer le Risque de Diabète'}
          </button>
        </form>

        {/* Affichage des messages d'erreur */}
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {/* Affichage des résultats de prédiction */}
        {prediction && prediction.success && (
          <div className="prediction-result">
            <h3>Résultat de l'Évaluation</h3>
            
            {/* Résultat principal */}
            <div className={`result-card ${prediction.prediction === 1 ? 'positive' : 'negative'}`}>
              <h4>{prediction.prediction_label}</h4>
              <p><strong>Niveau de risque:</strong> {prediction.risk_level}</p>
              <p><strong>Confiance:</strong> {(prediction.confidence * 100).toFixed(1)}%</p>
            </div>

            {/* Détails des probabilités */}
            <div className="probabilities-section">
              <h4>Détail des probabilités :</h4>
              <div className="probability-bars">
                <div className="probability-item">
                  <span className="probability-label">Pas de diabète:</span>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill no-diabetes" 
                      style={{width: `${(prediction.probabilities.no_diabetes * 100).toFixed(1)}%`}}
                    ></div>
                  </div>
                  <span className="probability-value">{(prediction.probabilities.no_diabetes * 100).toFixed(1)}%</span>
                </div>
                <div className="probability-item">
                  <span className="probability-label">Diabète:</span>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill diabetes" 
                      style={{width: `${(prediction.probabilities.diabetes * 100).toFixed(1)}%`}}
                    ></div>
                  </div>
                  <span className="probability-value">{(prediction.probabilities.diabetes * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>

            {/* ID Patient si disponible */}
            {prediction.patient_id && prediction.patient_id !== 'N/A' && (
              <div className="patient-info">
                <p><strong>ID Patient:</strong> {prediction.patient_id}</p>
              </div>
            )}

            {/* Recommandations selon le résultat */}
            {prediction.prediction === 1 ? (
              <div className="recommendation danger">
                <h4>⚠️ Recommandation importante</h4>
                <p>Les symptômes indiquent un risque élevé de diabète. Il est <strong>fortement recommandé</strong> de consulter un professionnel de santé dans les plus brefs délais pour des examens complémentaires (glycémie, HbA1c).</p>
              </div>
            ) : (
              <div className="recommendation safe">
                <h4>✅ Résultat rassurant</h4>
                <p>Selon l'analyse des symptômes, le risque de diabète semble faible. Continuez à maintenir un mode de vie sain et consultez régulièrement votre médecin pour des bilans préventifs.</p>
              </div>
            )}

            {/* Bouton pour nouvelle évaluation */}
            <button 
              onClick={() => {
                setPrediction(null);
                setFormData({
                  age: '', gender: '', polyuria: '', polydipsia: '',
                  sudden_weight_loss: '', weakness: '', polyphagia: '',
                  genital_thrush: '', visual_blurring: '', itching: '',
                  irritability: '', delayed_healing: '', partial_paresis: '',
                  muscle_stiffness: '', alopecia: '', obesity: ''
                });
              }}
              className="reset-btn"
            >
              Faire une nouvelle évaluation
            </button>
          </div>
        )}
      </section>
            <footer>
        <div className="footer-content">
          <div className="footer-social">
            <h3>Suivez-nous</h3>
            <div className="social-icons">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                <img src={facebookIcon} alt="Facebook" className="social-icon" />
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                <img src={instagramIcon} alt="Instagram" className="social-icon" />
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
                <img src={twitterIcon} alt="Twitter" className="social-icon" />
              </a>
              <a href="https://youtube.com" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
                <img src={youtubeIcon} alt="YouTube" className="social-icon" />
              </a>
            </div>
          </div>
          <div className="footer-info">
            <p>&copy; 2025 - Tous droits réservés</p>
            <p>Centre Hospitalier Felix Guichard</p>
          </div>
        </div>
      </footer>
    </>
  )
}

export default App
