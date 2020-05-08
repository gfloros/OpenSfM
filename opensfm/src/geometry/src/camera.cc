#include <geometry/camera.h>
#include <geometry/camera_functions.h>

Camera Camera::CreatePerspective(double focal, double k1, double k2) {
  Camera camera;
  camera.type_ = Type::PERSPECTIVE;
  camera.affine_ << focal, 0, 0, focal;
  camera.distortion_ << k1, k2, 0, 0, 0;
  return camera;
};

Camera Camera::CreateBrownCamera(double focal_x, double focal_y,
                                 const Eigen::Vector2d& principal_point,
                                 const Eigen::VectorXd& distortion) {
  Camera camera;
  if (distortion.size() != camera.distortion_.size()) {
    throw std::runtime_error("Invalid distortion coefficients size");
  }
  camera.type_ = Type::BROWN;
  camera.affine_ << focal_x, 0, 0, focal_y;
  camera.distortion_ = distortion;
  camera.principal_point_ = principal_point;
  return camera;
};

Camera Camera::CreateFisheyeCamera(double focal, double k1, double k2) {
  Camera camera;
  camera.type_ = Type::FISHEYE;
  camera.affine_ << focal, 0, 0, focal;
  camera.distortion_ << k1, k2, 0, 0, 0;
  return camera;
};

Camera Camera::CreateDualCamera(double transition, double focal, double k1, double k2) {
  Camera camera;
  camera.type_ = Type::DUAL;
  camera.projection_[0] = transition;
  camera.affine_ << focal, 0, 0, focal;
  camera.distortion_ << k1, k2, 0, 0, 0;
  return camera;
};

Camera Camera::CreateSphericalCamera() {
  Camera camera;
  camera.type_ = Type::SPHERICAL;
  return camera;
};

void Camera::SetDistortion(const Eigen::VectorXd& distortion) {
  std::vector<int> coeffs;
  if (type_ != Type::SPHERICAL) {
    coeffs.push_back(Disto::K1);
    coeffs.push_back(Disto::K2);
  }
  if (type_ == Type::BROWN) {
    coeffs.push_back(Disto::K3);
    coeffs.push_back(Disto::P1);
    coeffs.push_back(Disto::P2);
  }
  for (const auto idx : coeffs) {
    distortion_[idx] = distortion[idx];
  }
}
Eigen::VectorXd Camera::GetDistortion() const { return distortion_; }

void Camera::SetPrincipalPoint(const Eigen::Vector2d& principal_point) {
  if (type_ != Type::BROWN) {
    return;
  }
  principal_point_ = principal_point;
}
Eigen::Vector2d Camera::GetPrincipalPoint() const { return principal_point_; }

void Camera::SetFocal(double focal) {
  if (type_ == Type::SPHERICAL) {
    return;
  }

  const auto ar = GetAspectRatio();
  affine_(1, 1) = ar * focal;
  affine_(0, 0) = focal;
}
double Camera::GetFocal() const { return affine_(0, 0); }

void Camera::SetAspectRatio(double ar) { affine_(1, 1) = ar * GetFocal(); }

double Camera::GetAspectRatio() const { return affine_(1, 1) / affine_(0, 0); }

Eigen::Vector2d Camera::Project(const Eigen::Vector3d& point) const {
  return Dispatch<Eigen::Vector2d, ProjectT, Eigen::Vector3d>(
      type_, point, projection_, affine_, principal_point_, distortion_);
}

Eigen::MatrixX2d Camera::ProjectMany(const Eigen::MatrixX3d& points) const {
  Eigen::MatrixX2d projected(points.rows(), 2);
  for (int i = 0; i < points.rows(); ++i) {
    projected.row(i) = Project(points.row(i));
  }
  return projected;
}

Eigen::Vector3d Camera::Bearing(const Eigen::Vector2d& point) const {
  return Dispatch<Eigen::Vector3d, BearingT, Eigen::Vector2d>(
      type_, point, projection_, affine_, principal_point_, distortion_);
}

Eigen::MatrixX3d Camera::BearingsMany(const Eigen::MatrixX2d& points) const {
  Eigen::MatrixX3d projected(points.rows(), 3);
  for (int i = 0; i < points.rows(); ++i) {
    projected.row(i) = Bearing(points.row(i));
  }
  return projected;
}

Camera::Camera() : type_(Type::PERSPECTIVE) {
  projection_.resize(1);
  projection_[0] = 1.0;
  affine_.setIdentity();
  principal_point_.setZero();
  distortion_.resize(5);
  distortion_.setZero();
}