
//C++
#include <string.h>
#include <vector>

//DD4hep
#include "DDG4/Geant4SensDetAction.inl"
#include "DDG4/Factories.h"

namespace dd4hep {
  namespace sim {

    class ParticleCounter {
    public:

      Geant4Sensitive *sensitive = 0;

      ParticleCounter() {
        Info("SD", "ParticleCounter::ParticleCounter");
      }//ParticleCounter

      G4bool process(const G4Step* step) {

        //only particle counter hits
        std::string vnam = step->GetPostStepPoint()->GetPhysicalVolume()->GetName();
        if( vnam.find("ParticleCounter") == std::string::npos ) {
          Info("SD", "Not a counter volume: %s", vnam.c_str());
          return true;
        }

        //remove the track incident on the counter
        G4Track *track = step->GetTrack();
        track->SetTrackStatus(fKillTrackAndSecondaries);

        //energy in current step, including possible secondaries
        G4double en_step = track->GetTotalEnergy();

        //add possible secondaries to the energy
        const std::vector<const G4Track*> *sec = step->GetSecondaryInCurrentStep();
        std::vector<const G4Track*>::const_iterator isec = sec->begin();
        while(isec != sec->end()) {
          en_step += (*isec)->GetTotalEnergy();
          isec++;
        }

        //create the hit
        int track_id = track->GetTrackID();
        int track_pdg = track->GetDynamicParticle()->GetPDGcode();
        Geant4Tracker::Hit *hit = new Geant4Tracker::Hit(track_id, track_pdg, en_step, 0);

        //hit position
        const G4ThreeVector hp = step->GetPostStepPoint()->GetPosition();
        hit->position = Position(hp.x(), hp.y(), hp.z());

        Info("SD", "%s, %f, %f, %f, %f", vnam.c_str(), en_step, hp.x(), hp.y(), hp.z());

        Geant4HitCollection *collection = sensitive->collection(0);
        collection->add(hit);

        return true;
      }//process


    };//ParticleCounter

    //initialization
    template <> void Geant4SensitiveAction<ParticleCounter>::initialize() {
      m_userData.sensitive = this;
    }

    //hit collection
    template <> void Geant4SensitiveAction<ParticleCounter>::defineCollections() {
      m_collectionID = declareReadoutFilteredCollection<Geant4Tracker::Hit>();
    }

    //stepping callback
    template <> G4bool
    Geant4SensitiveAction<ParticleCounter>::process(G4Step *step, G4TouchableHistory* /*history*/) {
      return m_userData.process(step);
    }

    typedef Geant4SensitiveAction<ParticleCounter> ParticleCounterSDAction;

  }//sim
}//dd4hep

DECLARE_GEANT4SENSITIVE(ParticleCounterSDAction)

