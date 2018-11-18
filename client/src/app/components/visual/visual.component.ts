import { Component, OnInit } from '@angular/core';
import * as d3 from "d3";
import { Plot } from '../../canonicals/Plot';
import { DataService } from '../../service/data-service.service';
import { PlotPoint } from 'src/app/canonicals/PlotPoint';
import { delay } from 'q';
import { Extent } from 'src/app/canonicals/Extent';

@Component({
  selector: 'app-visual',
  templateUrl: './visual.component.html',
  styleUrls: ['./visual.component.css']
})
export class VisualComponent implements OnInit {
  points: PlotPoint[] = [];
  comparisons: PlotPoint[][] = [];
  window: Extent;
  loading: boolean;
  liveWindow: Extent;
  wells: string[]= [
    "6307_d"
  ];
  selectedWell: string;

  constructor(
    private dataService: DataService) {
  }

  ngOnInit() {
    this.observeWindow();
  }

  loadWell(): void {
    this.points = [];
    this.comparisons = [];
    this.loading = true;
    this.dataService.getPlot(this.selectedWell).then((response: PlotPoint[]) => {
      this.loading = false;
      this.points = response;
    }).catch((error) => console.log(error));
  }

  retrieveMatches(): void {
    this.dataService.retrieveMatches(this.selectedWell, this.window.From, this.window.To).then((response: PlotPoint[][]) => {
      this.comparisons = response;
    });
  }

  observeWindow(): any {
    this.dataService.getWindow().subscribe((response: Extent) => {
      this.liveWindow = response;
    });
  }

  async showWindow() {
    this.window = null;
    await delay(1000);
    this.window = this.liveWindow;
  }
}
