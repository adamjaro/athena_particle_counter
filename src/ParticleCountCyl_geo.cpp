
//C++

//DD4hep
#include "DD4hep/DetFactoryHelper.h"

using namespace dd4hep;

static Ref_t create_element(Detector& desc, xml_h e, SensitiveDetector sens)  {

  Info("ParticleCountCyl", "Creating the detector");

  xml_det_t x_det = e;
  std::string name = x_det.nameStr();

  Info("ParticleCountCyl", "Detector name: %s", name.c_str());
  Info("ParticleCountCyl", "Detector ID: %d", x_det.id());

  //counter shape
  xml_dim_t dim = x_det.dimensions();
  Tube shape(dim.r(), dim.r()+dim.dr(), dim.z()/2);
  //Box shape(100*mm, 100*mm, 100*mm);
  Volume vol(name+"_vol", shape, desc.material("LeadOxide"));
  vol.setVisAttributes(desc.visAttributes("TrackerVis"));

  sens.setType("tracker");
  vol.setSensitiveDetector(sens);

  //get the envelope volume
  //VolumeManager man = desc.volumeManager();
  VolumeManager man = VolumeManager::getVolumeManager(desc);
  //PlacedVolume pevol = man.lookupVolumePlacement( 3003 );
  //PlacedVolume pevol = man.lookupDetElementPlacement( 3003 );
  //DetElement pevol = man.lookupDetector( 3003 );
  DetElement wvol = man.detector();
  //std::map<std::string, DetElement>::iterator it = wvol.children().begin();
  auto it = wvol.children().begin();
  if( it == wvol.children().end() ) {

    Info("ParticleCountCyl", "Empty map");

  }
  while( it != wvol.children().end() ) {

    Info("ParticleCountCyl", "Child: %s", (*it).first.c_str());

    it++;
  }

  //std::string envelope_name = dd4hep::getAttrOrDefault(x_det, _Unicode(envelope), "dddfffggg");
  std::string envelope_name = dd4hep::getAttrOrDefault(x_det, _Unicode(envelope), "");
  Info("ParticleCountCyl", "Envelope name from xml: %s", envelope_name.c_str());

  //DetElement edet = wvol.child("CounterBox");
  DetElement edet = wvol.child(envelope_name);
  Volume evol = edet.volume();
  //DetElement env("CounterBox", 3003);
  //VolumeID eid = env.volumeID();
  //PlacedVolume pevol = man.lookupVolumePlacement( eid );
  Info("ParticleCountCyl", "Envelope placed volume: %s", evol.name());

  //top volume material
  DetElement det(name, x_det.id());
  Volume mvol = desc.pickMotherVolume( det );
  Info("ParticleCountCyl", "Mother volume name: %s", mvol.name());
  mvol.setMaterial(desc.material("Vacuum"));

  //placement in top volume
  //Transform3D pos(RotationZYX(0, 0, 0), Position(0, 0, 0));
  //PlacedVolume pv = mvol.placeVolume(vol, pos);

  //placement in envelope
  Transform3D pos(RotationZYX(0, 0, 0), Position(0, 0, 0));
  PlacedVolume pv = evol.placeVolume(vol, pos);

  pv.addPhysVolID("system", x_det.id());
  det.setPlacement(pv);

  return det;

}//create_element

DECLARE_DETELEMENT(ParticleCountCyl, create_element)































