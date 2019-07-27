import UIKit
import NMAKit

class MapViewController: UIViewController, UISearchResultsUpdating {
    let locationManager = CLLocationManager()
    
    @IBOutlet weak var mapView: NMAMapView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let geoCoordCenter = NMAGeoCoordinates(latitude: 0,
                                               longitude: 0)
        self.mapView.set(geoCenter: geoCoordCenter, animation: .none)
        self.mapView.copyrightLogoPosition = NMALayoutPosition.bottomCenter
        self.mapView.zoomLevel = 10
        
        self.locationManager.delegate = self
        self.locationManager.requestWhenInUseAuthorization()
        self.locationManager.startUpdatingLocation()
        
        Gradient().setGradientToNavigationBar(viewController: self)
        
        let searchController = UISearchController(searchResultsController: nil)
        self.navigationItem.titleView = searchController.searchBar
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.navigationController?.view.endEditing(true)
    }
    
    func updateSearchResults(for searchController: UISearchController) {
        if let text = searchController.searchBar.text {
            let a = CLGeocoder()
            a.geocodeAddressString(text) { (placemark, _) in
                print(placemark?[0])
            }
        }
    }
}

extension MapViewController: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        let location = locations.last
        let geoCordCenter = NMAGeoCoordinates(latitude: (location?.coordinate.latitude)!, longitude: (location?.coordinate.longitude)!)
        mapView.set(geoCenter: geoCordCenter, animation: .linear)
        self.locationManager.stopUpdatingLocation()
    }
}
