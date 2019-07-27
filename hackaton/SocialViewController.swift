import UIKit
import Charts

class SocialViewController: UIViewController {

    @IBOutlet weak var pieChart: PieChartView!
    @IBOutlet weak var starImage: UIImageView!
    
    var positiveReviewEntry = PieChartDataEntry(value: 20, label: "🔥")
    var negativeReviewEntry = PieChartDataEntry(value: 10, label: "💩")
    
    var numberOfDownloadsDataEntries = [PieChartDataEntry]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        numberOfDownloadsDataEntries = [positiveReviewEntry, negativeReviewEntry]
        updateChartData()
        Gradient().setGradientToNavigationBar(viewController: self)
    }
    
    func updateChartData() {
        let chartDataSet = PieChartDataSet(entries: numberOfDownloadsDataEntries, label: nil)
        let chartData = PieChartData(dataSet: chartDataSet)
        
        let colors = [#colorLiteral(red: 0.1108919606, green: 0.268920362, blue: 0.9908598065, alpha: 1), #colorLiteral(red: 0.9582478404, green: 0.2174702287, blue: 0.09099913388, alpha: 1)]
        
        chartDataSet.colors = colors
        
        pieChart.usePercentValuesEnabled = true
        pieChart.data = chartData
    }
}
