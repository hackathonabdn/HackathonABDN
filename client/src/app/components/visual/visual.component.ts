import { Component, OnInit } from '@angular/core';
import * as d3 from "d3";
import { Plot } from '../../canonicals/Plot';
import { DataService } from '../../service/data-service.service';
import { PlotPoint } from 'src/app/canonicals/PlotPoint';
import { delay } from 'q';

@Component({
  selector: 'app-visual',
  templateUrl: './visual.component.html',
  styleUrls: ['./visual.component.css']
})
export class VisualComponent implements OnInit {
  points: PlotPoint[] = [];
  window: PlotPoint[] = [];
  liveWindow: PlotPoint[] = [];

  constructor(
    private dataService: DataService) {
    this.observeWindow();
  }

  observeWindow(): any {
    this.dataService.getWindow().subscribe((response: PlotPoint[]) => {
      this.liveWindow = response;
    });
  }

  ngOnInit() {
    this.dataService.getPlot().then((response: PlotPoint[]) => {
      this.points = response;
    }).catch((error) => console.log(error));
  }

  async showWindow() {
    this.window = [];
    await delay(1000);
    this.window = this.liveWindow;
  }
}
