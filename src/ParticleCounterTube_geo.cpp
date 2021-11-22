
//C++

//DD4hep
#include "DD4hep/DetFactoryHelper.h"

using namespace dd4hep;

static Ref_t create_element(Detector& desc, xml_h e, SensitiveDetector sens)  {

  Info("ParticleCounter", "Creating the detector");

  xml_det_t x_det = e;
  std::string name = x_det.nameStr();

  Info("ParticleCounter", "Detector name: %s", name.c_str());
  Info("ParticleCounter", "Detector ID: %d", x_det.id());

  //counter shape
  xml_dim_t dim = x_det.dimensions();
  //Box shape(dim.x(), dim.y(), dim.z());
  Tube shape(dim.inner_r(), dim.outer_r(), dim.z()/2);
  Volume vol(name+"_vol", shape, desc.material("LeadOxide"));
  vol.setVisAttributes(desc.visAttributes("TrackerVis"));

  sens.setType("tracker");
  vol.setSensitiveDetector(sens);

  //mother volume for the counter
  std::string mother_nam = dd4hep::getAttrOrDefault(x_det, _Unicode(place_into), "");
  VolumeManager man = VolumeManager::getVolumeManager(desc);
  DetElement mdet = man.detector().child(mother_nam);

  //placement in mother volume
  xml_dim_t pos = x_det.position();
  Transform3D tr(RotationZYX(0, 0, 0), Position(pos.x(), pos.y(), pos.z()));
  PlacedVolume detPV = mdet.volume().placeVolume(vol, tr);
  detPV.addPhysVolID("system", x_det.id());
  DetElement det(name.c_str(), x_det.id());
  det.setPlacement(detPV);

  return det;

}//create_element

DECLARE_DETELEMENT(ParticleCounterTube, create_element)































