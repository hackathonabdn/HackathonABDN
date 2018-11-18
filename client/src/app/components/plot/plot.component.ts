import { Component, OnInit, Input } from '@angular/core';
import * as d3 from "d3";
import { Plot } from 'src/app/canonicals/Plot';
import { PlotPoint } from 'src/app/canonicals/PlotPoint';
import { DataService } from 'src/app/service/data-service.service';

@Component({
  selector: 'plot',
  templateUrl: './plot.component.html',
  styleUrls: ['./plot.component.css']
})
export class PlotComponent implements OnInit {
  @Input() id: string;
  @Input() selector: boolean;
  @Input() points: PlotPoint[];

  private x: any;
  private y: any;
  private brush: any;
  private dot: any;
  private width: number;
  private height: number;

  constructor(
    private dataService: DataService) {

  }

  ngOnInit() {
    this.renderPlot();
  }

  renderPlot(): void {
    let max = Math.max(...this.points.map(x => x.x));
    let min = Math.min(...this.points.map(x => x.x));
    let data = this.points.map(point => [point.x, point.y]);

    let randomX = d3.randomUniform(0, 10);
    let randomY = d3.randomNormal(0.5, 0.12);
    //let data = d3.range(800).map(function () { return [randomX(), randomY()]; });

    let svg = d3.select(`#${this.id}`).append("svg:svg").attr("width", 1110).attr("height", 200);
    let margin = { top: 20, right: 10, bottom: 30, left: 10 };
    let g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    this.width = +svg.attr("width") - margin.left - margin.right;
    this.height = +svg.attr("height") - margin.top - margin.bottom;

    this.x = d3.scaleLinear().range([0, this.width]);
    this.y = d3.scaleLinear().range([this.height, 0]);

    // Scale the range of the data
    this.x.domain(d3.extent(this.points, function (d) { return d.x; }));
    this.y.domain([0, d3.max(this.points, function (d) { return d.y; })]);

    let brushed: (xy, z) => void = () => {
      let extent = d3.event.selection.map(this.x.invert, this.x);
      let window = this.points.filter(point => point.x > extent[0] && point.x <= extent[1]);
      this.dataService.setWindow(window);
      this.dot.classed("selected", function (d) { return extent[0] <= d[0] && d[0] <= extent[1]; });
    }

    let brushcentered: (x, y, z) => void = () => {
      let dx = this.x(1) - this.x(0), // Use a fixed width when recentering.
        cx = d3.mouse(d3.event.currentTarget)[0],
        x0 = cx - dx / 2,
        x1 = cx + dx / 2;
      d3.select(d3.event.currentTarget.parentNode).call(this.brush.move, x1 > this.width ? [this.width - dx, this.width] : x0 < 0 ? [0, dx] : [x0, x1]);
    }

    this.brush = d3.brushX()
      .extent([[0, 0], [this.width, this.height]])
      .on("start brush", brushed);

    let self = this;

    this.dot = g.append("g")
      .attr("fill-opacity", 1)
      .selectAll("circle")
      .data(data)
      .enter().append("circle")
      .attr("transform", function (d) { return "translate(" + self.x(d[0]) + "," + self.y(d[1]) + ")"; })
      .attr("r", 0.75);

    if (this.selector) {
      g.append("g")
        .call(this.brush)
        .call(this.brush.move, [min, max].map(this.x))
        .selectAll(".overlay")
        .each(function (d: any) { d.type = "selection"; }) // Treat overlay interaction as move.
        .on("mousedown touchstart", brushcentered); // Recenter before brushing.
    }

    g.append("g")
      .attr("transform", "translate(0," + this.height + ")")
      .call(d3.axisBottom(this.x));
  }
}